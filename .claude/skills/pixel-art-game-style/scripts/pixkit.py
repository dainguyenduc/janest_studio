#!/usr/bin/env python3
"""pixkit.py — dựng sprite pixel art theo style bible cho MCP pixel-art.

Lệnh:
  ramp  --base 3e8948 --n 5           -> in ramp hue-shift (tối->sáng)
  tree  --out art/props/tree.png      -> cây 32x32 preset Cozy, in rows/legend DB16 gần nhất
  tile  --src t.png --out t_3x3.png   -> ghép 3x3 để soi seamless
  sheet --frames f00.png f01.png --out sheet.png

Không cần cài gì thêm: PNG I/O thuần Python (zlib trong stdlib). Hỗ trợ đọc PNG
8-bit color type 0/2/3/6. Nếu gặp định dạng khác, hãy chuyển về PNG 8-bit trước.
"""
import argparse, colorsys, json, math, os, struct, zlib

DB16 = ["000000", "ffffff", "9d9d9d", "be2633", "e06f8b", "493c2b", "a46422", "eb8931",
        "f7e26b", "2f484e", "44891a", "a3ce27", "1b2632", "005784", "31a2f2", "b2dcef"]
LIGHT = (-0.55, -0.65, 0.52)  # nguồn sáng trên-trái, hướng về người xem


# --------------------------------------------------------------------------
# PNG I/O thuần Python (thay cho Pillow)
# --------------------------------------------------------------------------
def _png_write(path, w, h, buf):
    """buf: bytes/bytearray độ dài w*h*4 (RGBA, hàng trên xuống)."""
    stride = w * 4
    raw = bytearray()
    for y in range(h):
        raw.append(0)  # filter type 0
        raw += buf[y * stride:(y + 1) * stride]

    def chunk(typ, data):
        return struct.pack(">I", len(data)) + typ + data + \
            struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff)

    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)))
        f.write(chunk(b"IDAT", zlib.compress(bytes(raw), 9)))
        f.write(chunk(b"IEND", b""))


def _paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    return a if pa <= pb and pa <= pc else (b if pb <= pc else c)


def _png_read(path):
    """Trả về (w, h, bytearray RGBA). Hỗ trợ bit depth 8, color type 0/2/3/6."""
    data = open(path, "rb").read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "không phải PNG"
    i = 8
    w = h = depth = ctype = 0
    idat = bytearray()
    plte = None
    trns = None
    while i < len(data):
        ln = struct.unpack(">I", data[i:i + 4])[0]
        typ = data[i + 4:i + 8]
        chunk = data[i + 8:i + 8 + ln]
        i += 12 + ln
        if typ == b"IHDR":
            w, h, depth, ctype = struct.unpack(">IIBB", chunk[:10])
        elif typ == b"PLTE":
            plte = chunk
        elif typ == b"tRNS":
            trns = chunk
        elif typ == b"IDAT":
            idat += chunk
        elif typ == b"IEND":
            break
    assert depth == 8, "chỉ hỗ trợ PNG 8-bit (chuyển đổi trước khi dùng)"
    ch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    stride = w * ch
    raw = zlib.decompress(bytes(idat))
    out = bytearray()
    prev = bytearray(stride)
    pos = 0
    for _ in range(h):
        f = raw[pos]; pos += 1
        line = bytearray(raw[pos:pos + stride]); pos += stride
        for x in range(stride):
            a = line[x - ch] if x >= ch else 0
            b = prev[x]
            c = prev[x - ch] if x >= ch else 0
            if f == 1: line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + b) & 255
            elif f == 3: line[x] = (line[x] + ((a + b) >> 1)) & 255
            elif f == 4: line[x] = (line[x] + _paeth(a, b, c)) & 255
        out += line; prev = line
    # -> RGBA
    rgba = bytearray(w * h * 4)
    for px in range(w * h):
        o = px * ch
        if ctype == 6:
            rgba[px * 4:px * 4 + 4] = out[o:o + 4]
        elif ctype == 2:
            rgba[px * 4:px * 4 + 3] = out[o:o + 3]; rgba[px * 4 + 3] = 255
        elif ctype == 0:
            v = out[o]; rgba[px * 4:px * 4 + 4] = bytes((v, v, v, 255))
        elif ctype == 3:
            idx = out[o]
            r, g, b = plte[idx * 3:idx * 3 + 3]
            a = trns[idx] if trns and idx < len(trns) else 255
            rgba[px * 4:px * 4 + 4] = bytes((r, g, b, a))
    return w, h, rgba


class Img:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.buf = bytearray(w * h * 4)  # mặc định trong suốt

    def put(self, x, y, rgba):
        if 0 <= x < self.w and 0 <= y < self.h:
            o = (y * self.w + x) * 4
            self.buf[o:o + 4] = bytes(rgba)

    def paste(self, other, ox, oy):
        for y in range(other.h):
            o = (y * other.w) * 4
            row = other.buf[o:o + other.w * 4]
            for x in range(other.w):
                self.put(ox + x, oy + y, row[x * 4:x * 4 + 4])

    def resize_nearest(self, nw, nh):
        out = Img(nw, nh)
        for y in range(nh):
            sy = y * self.h // nh
            for x in range(nw):
                sx = x * self.w // nw
                o = (sy * self.w + sx) * 4
                oo = (y * nw + x) * 4
                out.buf[oo:oo + 4] = self.buf[o:o + 4]
        return out

    def save(self, path):
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        _png_write(path, self.w, self.h, self.buf)

    @staticmethod
    def open(path):
        w, h, rgba = _png_read(path)
        im = Img(w, h); im.buf = rgba
        return im


# --------------------------------------------------------------------------
# Màu & ramp hue-shift
# --------------------------------------------------------------------------
def rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexs(c):
    return "%02x%02x%02x" % c


def mcp_color(h, a=255):
    """hex rrggbb -> 'aarrggbb' cho pyxel_set_pixel / pyxel_flood_fill."""
    return "%02x%s" % (a, h.lstrip('#').lower())


def _toward(hd, target, step):
    d = (target - hd + 540) % 360 - 180
    return target if abs(d) <= step else (hd + math.copysign(step, d)) % 360


def hue_ramp(base, n=5, step=15, v_lo=0.22, v_hi=0.96, warm=55, cool=245):
    """Ramp tối->sáng: sáng ngả về vàng (warm), tối ngả về lam/tím (cool),
    bão hoà đỉnh ở giữa. Dựa trên Slynyrd Pixelblog #1 (hue-shift <=20 deg/bước)."""
    r, g, b = [x / 255 for x in rgb(base)]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h *= 360
    mid = (n - 1) / 2
    out = []
    for i in range(n):
        k = i - mid
        hh = h
        for _ in range(int(abs(k))):
            hh = _toward(hh, warm if k > 0 else cool, step)
        ss = max(0.0, min(1.0, s * (1 - 0.35 * abs(k) / max(mid, 1))))
        vv = v_lo + (v_hi - v_lo) * i / (n - 1)
        c = colorsys.hsv_to_rgb(hh / 360, ss, vv)
        out.append(hexs(tuple(round(x * 255) for x in c)))
    return out


def _norm(v):
    l = math.sqrt(sum(a * a for a in v))
    return tuple(a / l for a in v)


def nearest_db16(h):
    c = rgb(h)
    return min(range(16), key=lambda i: sum((a - b) ** 2 for a, b in zip(c, rgb(DB16[i]))))


# --------------------------------------------------------------------------
# Sprite: khối, bóng theo hướng sáng, outline, sel-out, dọn mồ côi
# --------------------------------------------------------------------------
class Sprite:
    """Lưới (material, tone). tone>=0: tông trong ramp[tone+1]; -1: outline ramp[0]; -2: sel-out ramp[1]."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.px = [[None] * w for _ in range(h)]

    def inside(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h

    def put(self, x, y, mat, tone):
        if self.inside(x, y):
            self.px[y][x] = (mat, tone)

    def ball(self, cx, cy, rx, ry, mat, tones, light=LIGHT, bias=0.0):
        """Ellipse đổ bóng Lambert theo hướng sáng -> không bị pillow shading."""
        L = _norm(light)
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                nx = (x + 0.5 - cx) / rx
                ny = (y + 0.5 - cy) / ry
                d = nx * nx + ny * ny
                if d > 1:
                    continue
                nz = math.sqrt(1 - d)
                lam = max(0.0, nx * L[0] + ny * L[1] + nz * L[2]) + bias
                self.put(x, y, mat, min(tones - 1, max(0, int(lam * tones))))

    def column(self, x0, y0, x1, y1, mat, tones, light_from_left=True):
        """Khối trụ đứng (thân cây, cột): sáng phía trái, tối phía phải."""
        w = x1 - x0 + 1
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                u = (x - x0 + 0.5) / w
                lit = 1 - u if light_from_left else u
                self.put(x, y, mat, min(tones - 1, int(lit * tones)))

    def clean_orphans(self):
        """Pixel khác hẳn 4 hàng xóm -> nhập vào tông phổ biến nhất của cùng vật liệu."""
        for y in range(self.h):
            for x in range(self.w):
                p = self.px[y][x]
                if p is None or p[1] < 0:
                    continue
                ns = [self.px[y + dy][x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                      if self.inside(x + dx, y + dy) and self.px[y + dy][x + dx] is not None]
                if ns and all(n != p for n in ns):
                    same = [n for n in ns if n[0] == p[0] and n[1] >= 0]
                    if same:
                        self.px[y][x] = max(set(same), key=same.count)

    def outline(self, conn=8, selout=True):
        """Outline màu = ramp[0] của vật liệu kề bên; sel-out: viền phía trên/trái dùng ramp[1]."""
        n4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        nb = n4 + [(1, 1), (1, -1), (-1, 1), (-1, -1)] if conn == 8 else n4
        add = {}
        for y in range(self.h):
            for x in range(self.w):
                if self.px[y][x] is not None:
                    continue
                dirs = [(dx, dy) for dx, dy in nb
                        if self.inside(x + dx, y + dy) and self.px[y + dy][x + dx] is not None]
                if not dirs:
                    continue
                dx0, dy0 = dirs[0]
                mat = self.px[y + dy0][x + dx0][0]
                lit = selout and all(dx >= 0 and dy >= 0 for dx, dy in dirs)
                add[(x, y)] = (mat, -2 if lit else -1)
        for (x, y), v in add.items():
            self.px[y][x] = v

    def color_of(self, p, ramps):
        mat, t = p
        r = ramps[mat]
        return r[0] if t == -1 else r[1] if t == -2 else r[min(t + 1, len(r) - 1)]

    def save_png(self, path, ramps, scale=1):
        im = Img(self.w, self.h)
        for y in range(self.h):
            for x in range(self.w):
                p = self.px[y][x]
                if p is not None:
                    im.put(x, y, rgb(self.color_of(p, ramps)) + (255,))
        if scale > 1:
            im = im.resize_nearest(self.w * scale, self.h * scale)
        im.save(path)

    def to_rows(self, ramps):
        """rows/legend cho pyxel_draw (map về DB16 gần nhất) + bảng hex gốc để tô lại."""
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        cmap, legend, rows = {}, {}, []
        for y in range(self.h):
            row = ""
            for x in range(self.w):
                p = self.px[y][x]
                if p is None:
                    row += "."
                    continue
                h = self.color_of(p, ramps)
                if h not in cmap:
                    ch = chars[len(cmap)]
                    cmap[h] = ch
                    legend[ch] = nearest_db16(h)
                row += cmap[h]
            rows.append(row)
        return {"rows": rows, "legend": legend, "hex": {v: k for k, v in cmap.items()}}

    def to_set_pixel_ops(self, ramps, ox=0, oy=0):
        """Danh sách tham số pyxel_set_pixel (gọi song song; batch KHÔNG hỗ trợ set_pixel)."""
        return [{"x": x + ox, "y": y + oy, "color": mcp_color(self.color_of(p, ramps))}
                for y, row in enumerate(self.px) for x, p in enumerate(row) if p is not None]


# --------------------------------------------------------------------------
# Demo + tiện ích
# --------------------------------------------------------------------------
def demo_tree(out="art/props/tree_cozy_32.png"):
    ramps = {  # Endesga 32, tối->sáng, [0] = outline màu
        "leaf": ["193c3e", "265c42", "3e8948", "63c74d", "fee761"],
        "bark": ["3e2731", "733e39", "b86f50", "e4a672"],
    }
    s = Sprite(32, 32)
    s.column(14, 20, 17, 29, "bark", tones=3)
    for (cx, cy, r) in [(10, 15, 7), (22, 15, 7), (16, 12, 10)]:  # cụm phụ trước, cụm chính đè lên
        s.ball(cx, cy, r, r * 0.9, "leaf", tones=4)
    s.clean_orphans()
    s.outline(conn=8, selout=True)
    s.save_png(out, ramps)
    s.save_png(out.replace(".png", "_x8.png"), ramps, scale=8)
    return s, ramps


def tile_preview(src, out, n=3, scale=4):
    t = Img.open(src)
    w, h = t.w, t.h
    im = Img(w * n, h * n)
    for j in range(n):
        for i in range(n):
            im.paste(t, i * w, j * h)
    im.resize_nearest(w * n * scale, h * n * scale).save(out)


def make_sheet(frames, out):
    ims = [Img.open(f) for f in frames]
    w, h = ims[0].w, ims[0].h
    sh = Img(w * len(ims), h)
    for i, im in enumerate(ims):
        sh.paste(im, i * w, 0)
    sh.save(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["ramp", "tree", "tile", "sheet"])
    ap.add_argument("--base", default="3e8948")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--src")
    ap.add_argument("--frames", nargs="*")
    ap.add_argument("--out", default="art/props/tree_cozy_32.png")
    a = ap.parse_args()
    if a.cmd == "ramp":
        print(json.dumps(hue_ramp(a.base, a.n)))
    elif a.cmd == "tree":
        s, ramps = demo_tree(a.out)
        print(json.dumps(s.to_rows(ramps), ensure_ascii=False))
    elif a.cmd == "tile":
        tile_preview(a.src, a.out)
    else:
        make_sheet(sorted(a.frames), a.out)
