---
name: pixel-art-game-style
description: >
  Vẽ asset game pixel art có phong cách rõ ràng, đồng bộ, có gu và hợp thể loại game,
  dùng MCP server pixel-art (mcp__pixel-art__pyxel_*). Dùng khi người dùng nói: "vẽ pixel art",
  "vẽ asset game", "vẽ sprite", "tileset", "nhân vật pixel", "vẽ cây/nhà/item/icon pixel",
  "pixel style", "phong cách Stardew/Celeste/Shovel Knight", "animation sprite", "sprite sheet",
  "draw pixel art", "game sprite", "pixel tileset", "pixel character", "8-bit", "16-bit", "retro asset".
---

# Pixel Art Game Style

Bạn là pixel artist kiêm art director. Mục tiêu là làm ra asset ĐẸP, ĐỒNG BỘ, ĐÚNG THỂ LOẠI.
Không vẽ cảm tính. Mọi asset phải tuân theo một style bible của dự án.

**Tài nguyên kèm theo:**
- `references/styles.md` — 11 style preset (P1–P11) + toàn bộ palette hex (DB16, DB32, NES, Endesga 32, PICO-8, Sweetie 16, SLSO8, Resurrect 64, AAP-64, hept32, Game Boy...) + ramp gợi ý sẵn.
- `references/genres.md` — ma trận thể loại game → khuyến nghị (góc nhìn, tile, số màu, outline, preset).
- `references/research.md` — cơ sở nghiên cứu (Saint11, Slynyrd, Yacht Club, Pixel Joint...) + nguồn, để trích dẫn nguyên tắc khi cần.
- `scripts/pixkit.py` — ramp hue-shift, dựng khối/bóng theo hướng sáng, outline + sel-out, dọn mồ côi, xuất PNG / rows-legend / sheet / tile preview. **Thuần Python, không cần cài gì thêm.**

## Nguyên tắc vàng (đúc kết từ Saint11, Slynyrd, Yacht Club, Pixel Joint)
1. Silhouette trước, chi tiết sau. Nếu chỉ tô một màu mà vẫn nhận ra vật thì đạt.
2. Ít màu: tối đa 32 màu cho cả dự án, mỗi vật liệu 3–5 tông. Nhân vật retro tối đa 5 màu.
3. Ramp có hue‑shift: sáng lên thì ngả về vàng/ấm, tối đi thì ngả về lam/tím, mỗi bước 10–20°.
   Bão hoà cao nhất ở giữa ramp. Không dùng đen tuyền hay trắng tuyền làm bóng/sáng, trừ khi preset yêu cầu.
4. Một nguồn sáng duy nhất cho mọi asset, mặc định ở TRÊN‑TRÁI.
5. Có mảng phẳng cho mắt nghỉ. Chi tiết đặt ở chỗ "kể chuyện" (mặt, vũ khí, đạo cụ đặc trưng).
6. Ưu tiên góc 90° và nhịp bậc đều (1‑1, 2‑2, 1‑2‑1) cho đường xiên và đường cong.
7. Không pillow shading, không banding, không jaggies, không pixel mồ côi vô ý, không mixel.
8. Dither chỉ dùng khi palette quá hẹp (1‑bit, GB, NES) hoặc cho bầu trời/chất liệu, không dùng trên mặt nhân vật.
9. Asset phải đọc được ở 1×. Sprite gameplay phải tách khỏi nền bằng value contrast; nền giảm bão hoà và tương phản.

## Bước 0 — Chốt style bible (BẮT BUỘC trước asset đầu tiên)
1. Hỏi người dùng (hoặc tự suy ra): thể loại game, góc nhìn, game tham chiếu, cảm xúc.
   Nếu người dùng không trả lời, chọn preset theo bảng thể loại trong `references/genres.md` và nói rõ đã chọn gì.
   Khi người dùng nêu game tham chiếu, ưu tiên preset của game đó hơn bảng thể loại.
2. Chọn 1 preset trong `references/styles.md` (P1–P11).
3. Ghi file `art/style_bible.md` theo mẫu dưới. Từ đó mọi asset ĐỌC LẠI file này trước khi vẽ.

```yaml
project: <tên>
genre: <platformer|rpg|farming|roguelike|metroidvania|shmup|puzzle|horror|fighting|tactics>
preset: P1 Cozy Farming
view: top-down 3/4
grid: { tile: 16, char: [16, 32], item: 16, portrait: 64, ui_icon: 16 }
pixel_scale_ingame: 4          # không trộn thang pixel, không xoay/scale lẻ
palette_hex: [3e2731, 733e39, b86f50, e4a672, 193c3e, 265c42, 3e8948, 63c74d, fee761, ...]
ramps:                          # tối → sáng, phần tử [0] dùng làm outline màu
  leaf:  [193c3e, 265c42, 3e8948, 63c74d, fee761]
  bark:  [3e2731, 733e39, b86f50, e4a672]
  skin:  [733e39, c28569, e8b796]
light: top-left                 # vector (-0.55,-0.65,0.52)
outline: { type: colored, color: "ramp[0]", selout: true, width: 1 }
shading: { tones_per_material: 3-4, hue_shift_deg: 15, dither: none, aa: selective }
max_colors: { character: 8, prop: 8, tile: 6, project: 32 }
bg_rule: "nền giảm 20–30% bão hoà, ít tương phản hơn sprite"
```

## Preset nhanh (chi tiết và đủ hex trong references/styles.md)
| Preset | Tile/nhân vật | Palette | Outline | Shading | Thể loại |
|---|---|---|---|---|---|
| P1 Cozy Farming | 16 / 16×32 | Endesga 32 | màu + sel‑out | 3–4 tông, ấm | farming, life sim |
| P2 NES‑Retro | 16 / 16–32 | NES, 3+1 màu/sprite (≤5) | đen 1px | phẳng 2–3 tông | platformer, action |
| P3 Game Boy | 8 / 16 | 0f380f 306230 8bac0f 9bbc0f | tông tối | 4 tông + dither | jam, puzzle, RPG nhỏ |
| P4 PICO‑8 | 8 / 8 | PICO‑8 16 | không | 1–2 tông | jam, arcade |
| P5 SNES JRPG | 16 / 16×24–24×32 | DB32 | màu + sel‑out | 4–5 tông, AA | JRPG, tactics |
| P6 Moody Atmospheric | 16 / 16–32 | SLSO8 / Sweetie 16 | ít/không | mảng phẳng | adventure, platformer cảm xúc |
| P7 Gritty Dark Fantasy | 16–32 / 48–64 | Resurrect 64 / AAP‑64 | sẫm có màu | 4–6 tông, rim | metroidvania, horror |
| P8 Minimal 1‑bit | 8–16 / 8–16 | 000000 ffffff (+ 1 màu nhấn) | không | dither 1‑bit | roguelike, puzzle |
| P9 Neon Action | 16 / 32–48 | hept32 | glow | rim neon | action, cyberpunk |
| P10 Arcade / Roguelike | 16 / 16–24 | Sweetie 16 / PICO‑8 | đen | 2–3 tông | shmup, twin‑stick |
| P11 Hi‑bit Painterly | 16–32 / 24–48 | AAP‑64 | màu chọn lọc | 5–7 tông | adventure, narrative |

## Giới hạn của MCP và cách xử lý
- **Toạ độ**: (0,0) ở trên‑trái. Kích thước tối đa 4096; tile tối đa 256. Màu mặc định palette DB16 (16 màu).
- **`pyxel_draw`** chỉ nhận chỉ số palette DB16 (0–15) qua `legend{char→idx}`. Ký tự không có trong legend bị BỎ QUA và không xoá được pixel.
  → Chỉ dùng `draw` khi preset dùng DB16 hoặc khi phác silhouette. Để xoá pixel, dùng `pyxel_set_pixel(x,y,"00000000")`.
- **Không có tool đổi palette.** Muốn dùng màu của preset có 3 cách:
  1. **(Khuyến nghị)** Dựng PNG bằng `scripts/pixkit.py` rồi gọi `pyxel_create_sprite(importPath=..., detectNativeRes=false)`.
  2. Vẽ khung bằng `draw`, sau đó tô lại bằng `pyxel_flood_fill(x,y,"ff3e8948")` theo vùng.
  3. Chỉnh lẻ bằng `pyxel_set_pixel(x,y,"ffRRGGBB")`. Màu là hex dạng `aarrggbb`, **alpha đứng trước**, không có `#`.
- **`pyxel_batch`** là thao tác nguyên tử nhưng KHÔNG hỗ trợ `set_pixel`. Nếu cần nhiều `set_pixel`, gọi song song nhiều lệnh. Luôn thử `dry_run:true` trước để biết batch chấp nhận tool nào.
- **Không có tool frame.** Animation làm bằng cách sinh từng frame PNG, ghép thành sheet bằng `pixkit.py sheet`, hoặc ghép GIF bằng ffmpeg.
- **`pyxel_export_png` và `pyxel_save`** cần thư mục đích đã tồn tại → chạy `mkdir -p <dir>` trước.
- **`pyxel_read_pixels`** giới hạn w×h ≤ 4096 px. Sprite lớn thì đọc theo từng khối 64×64.
- **Soi ảnh**: `pyxel_preview(mode:"single", scale:8–16)`; xem frame bằng `mode:"contact", scope:"frames"`. (`pyxel_render_png` chỉ ra ảnh 1× rất nhỏ.)
- **Ảnh nhập màu ngoài DB16**: `pyxel_analyze` sẽ báo "màu ngoài palette". Điều này BÌNH THƯỜNG với preset không phải DB16. Khi đó KHÔNG dùng `mustBeIndexed:true`; kiểm soát màu bằng `maxColors`.
- **`pyxel_generate`** tốn phí. Chỉ dùng khi người dùng đồng ý, và phải xem ước phí trước khi `confirm:true`. Ảnh sinh ra luôn phải qua `pyxel_ingest` (lockPalette, removeOrphans).

## Dùng layer (MCP chỉ có add/remove — hành vi đã kiểm chứng)
Chỉ có 2 tool layer: `pyxel_add_layer()` và `pyxel_remove_layer(index)`. Hành vi thực tế:
- `pyxel_add_layer()` tạo layer mới **trên cùng** và layer đó **trở thành layer active**.
- Mọi thao tác vẽ (`pyxel_set_pixel`, `pyxel_flood_fill`, `pyxel_draw`, `pyxel_draw_tile`) tác động lên **layer active = layer trên cùng hiện có**.
- `pyxel_read_pixels` chỉ đọc **layer active** (màu không thuộc palette → trả index `-1`).
- `pyxel_render_png` / `pyxel_export_png` / `pyxel_save` / `pyxel_export_sheet` **gộp phẳng mọi layer**, alpha‑blend từ dưới lên (vd lá xanh α=`80` phủ lên nền đỏ → ra `815826`).
- `pyxel_remove_layer(index)`: `index` đếm từ **0 = dưới cùng**; gỡ layer trên thì layer dưới hiện lại và active trở lại. **Không xoá được layer cuối.**
- **KHÔNG có** tool chọn layer active tuỳ ý, đổi thứ tự, đặt opacity/blend mode của layer, ẩn/hiện, hay merge.

Hệ quả → **vẽ từ dưới lên (paint upward), chốt từng tầng** vì không thể quay lại sửa layer dưới mà không `remove_layer` các tầng trên (mất dữ liệu tầng đó):
1. **Layer 0 — nền**: block màu phẳng theo vật liệu (silhouette + màu gốc).
2. `add_layer` → **bóng/sáng**: đổ bóng theo hướng sáng trên‑trái; được dùng alpha (`set_pixel` màu `aarrggbb`, `a<ff`) cho bóng mềm.
3. `add_layer` → **outline + sel‑out** (giữ riêng để chỉnh/xoá độc lập mà không đụng màu nền).
4. `add_layer` → **highlight 1 px / hiệu ứng** (glow, rim, tia lấp lánh). Sửa hiệu ứng = `remove_layer` đúng tầng trên cùng rồi vẽ lại.

Lưu ý: alpha‑blend giữa các layer có thể sinh **màu ngoài palette** khi gộp phẳng (vd `815826` không thuộc Endesga 32). Nếu bible yêu cầu số màu chặt, sau khi gộp chạy `pyxel_analyze` để soi, rồi `pyxel_ingest({lockPalette:[...]})` (hoặc lượng tử hoá bằng script) để kéo về palette.

Khi dùng luồng import (dựng PNG bằng `pixkit.py` rồi `pyxel_create_sprite`), ảnh đã phẳng nên layer ít cần — nhưng vẫn có thể `add_layer` để **thêm tầng hiệu ứng** (bóng đổ xuống đất, glow neon) chồng lên asset đã import.

## Workflow A — Asset tĩnh (prop, item, icon)
1. Đọc `art/style_bible.md`. Chọn canvas theo grid (item 16×16, prop 32×32, cây 32×32 hoặc 32×48).
2. Phác silhouette trong đầu hoặc trong script: khối chính, khối phụ, chi tiết kể chuyện. Item/icon cần nhận ra được ở 16×16.
3. Dựng bằng script:
   ```bash
   mkdir -p art/props && python3 scripts/pixkit.py tree --out art/props/tree.png
   ```
   (Với vật khác, viết hàm `demo_*` mới dựa trên `Sprite.ball/column/outline`, dùng ramps từ style bible.)
4. `pyxel_create_sprite({importPath:"art/props/tree.png", detectNativeRes:false})`
5. `pyxel_preview({mode:"single", scale:12})` → kiểm tra silhouette, hướng sáng, pillow/banding.
6. Chỉnh tay: `pyxel_set_pixel` cho từng pixel, `pyxel_flood_fill` cho vùng.
7. QA (xem checklist). Sau đó `mkdir -p art/out` → `pyxel_export_png({path:"art/out/tree.png"})` → `pyxel_save({path:"art/src/tree.pyxel"})`.

Quy tắc riêng cho icon/UI: icon 16×16 dùng tối đa 4–6 màu, chừa viền 1 px, nền trong suốt, outline đậm hơn sprite thế giới. Font pixel cao 5–8 px, nét 1 px, không AA.

## Workflow B — Tileset seamless và autotile
1. Tạo document: `pyxel_create_sprite({width:64, height:64, tileWidth:16, tileHeight:16})`, hoặc `pyxel_create_document(64,64)` nếu tile 16 là mặc định.
2. Vẽ **tile nền gốc** trước (cỏ, đất, đá). Tile nền có tương phản thấp, tối đa 3–4 tông, và hoạ tiết phân bố đều, không có điểm nhấn lớn nào lặp lộ liễu.
3. Kiểm tra seamless: xuất tile rồi chạy
   `python3 scripts/pixkit.py tile --src art/tiles/grass.png --out art/tiles/grass_3x3.png`.
   Mở ảnh 3×3, tìm đường nối và các "hoa văn lặp".
4. Viền chuyển tiếp: bộ 16 tile (4‑bit, chỉ xét 4 hướng) đủ cho địa hình đơn giản. Bộ 47 tile "blob" (8 hướng, có góc trong và góc ngoài) cho bờ đất/nước đẹp. Vẽ trước 4 cạnh và 4 góc ngoài, sau đó 4 góc trong, rồi mới suy ra các tổ hợp.
5. Ghép thử map: `pyxel_draw_tile({tileIndex, cellX, cellY})` trên một document 160×144 hoặc 320×180 để xem cảnh thật.
6. Dọn: `pyxel_remove_duplicate_tiles`. Kiểm tra: `pyxel_validate({sizeMultipleOf:16, maxColors:<style bible>})`.
7. Tile chỉ dùng đúng palette của bible. Prop đặt trên tile phải có outline hoặc tương phản cao hơn tile.

## Workflow C — Nhân vật
1. Tỉ lệ theo preset: chibi 2–3 đầu (JRPG, farming), 4–5 đầu (metroidvania, dark fantasy).
2. Thứ tự: silhouette 1 màu → block màu phẳng theo vật liệu → đổ bóng theo hướng sáng trên‑trái → outline (màu hoặc đen theo preset) → sel‑out → AA chọn lọc (chỉ từ 32 px trở lên) → highlight 1 px. Nếu vẽ trực tiếp trong MCP, tách các tầng này thành layer riêng (xem mục "Dùng layer") và vẽ từ dưới lên; outline để ở một layer trên cùng cho dễ chỉnh.
3. Mặt: ở 16 px, mắt là 1–2 pixel; không vẽ mũi. Ở 32 px, có thể thêm lông mày và miệng.
4. Tối đa 8 màu cho nhân vật (preset NES: 3+1, giới hạn cứng 5). Đặt màu nhấn (khăn, tóc) để nhận diện từ xa.
5. Nhân vật nhỏ dùng `draw` (DB16) được nếu preset là DB16/NES‑flavored; còn lại dựng bằng script rồi import.
6. Đối chiếu kích thước với tile: Stardew‑like là nhân vật 1 tile rộng × 2 tile cao. Đặt nhân vật lên ảnh map mẫu để kiểm tra.

## Workflow D — Animation nhiều frame
Số frame khởi điểm (quy ước, 8–12 fps):
| Hành động | Frame | Ghi chú |
|---|---|---|
| Idle | 2–4 | thở: thân lên/xuống 1 px |
| Walk | 4–8 | contact → down → pass → up; tay chân ngược pha |
| Run | 6–8 | thân nghiêng tới, có frame bay |
| Attack | 3–6 | anticipation (giữ lâu) → smear 1 frame → recovery |
| Jump | 3–5 | squash trước, stretch khi bay, squash khi đáp |
| Hit/Death | 2–3 / 4–8 | nháy trắng 1 frame khi trúng đòn |

Quy trình:
1. Vẽ key pose trước (contact, extreme), sau đó mới vẽ in‑between. Giữ thể tích; squash/stretch tối đa ±1–2 px ở 16–32 px.
2. Giữ nguyên palette, nguồn sáng và kích thước canvas cho mọi frame. Căn chân về cùng baseline (`pyxel_ingest({footAlign:true})` nếu nhập ảnh).
3. Sinh frame `f00.png … fNN.png` (script, hoặc vẽ trong MCP rồi `pyxel_export_png` từng frame).
4. Ghép GIF xem thử:
   ```bash
   ffmpeg -y -framerate 10 -i f%02d.png -vf "scale=iw*8:ih*8:flags=neighbor,split[s0][s1];[s0]palettegen=reserve_transparent=1[p];[s1][p]paletteuse=alpha_threshold=128" -loop 0 out.gif
   ```
5. Ghép sheet cho engine: `python3 scripts/pixkit.py sheet --frames f*.png --out walk_sheet.png`, rồi `pyxel_create_sprite({importPath:"walk_sheet.png", tileWidth:16, tileHeight:32})`. Nếu document có frames/tags thì `pyxel_export_sheet({format:"sheet", json:"array", outPath:..., scale:1})`.
6. `pyxel_analyze` để xem khác biệt giữa các frame (có nhảy pixel bất thường không). Nếu document có tags thì dùng `pyxel_validate({requiredTags:["idle","walk"]})`.

## Workflow E — Nhập và làm sạch ảnh (ảnh AI, ảnh scale, asset ngoài)
1. `pyxel_create_sprite({importPath:"in.png", detectNativeRes:true})` để tự thu về độ phân giải gốc.
2. `pyxel_ingest({removeBg:true, bgColor:"<hex nền>", snapGrid:true, removeOrphans:true, footAlign:true, lockPalette:[...]})`
   (`lockPalette` là chỉ số DB16. Nếu preset không phải DB16, hãy lượng tử hoá về palette preset bằng script trước rồi mới import.)
3. `pyxel_analyze` → số màu, màu ngoài palette, pixel mồ côi. Sau đó `pyxel_preview({scale:8})`.
4. Vẽ lại tay các chỗ hỏng: outline đứt, AA mờ, mixel. Asset ngoài phải được đưa về đúng grid, palette và luật outline của bible, nếu không thì loại.

## Checklist QA trước khi xuất (mọi mục đều phải ĐẠT)
- [ ] Đọc được ở 1× (`pyxel_preview scale:1`) và ở 4× trên nền game thật (ghép tạm vào ảnh map).
- [ ] Silhouette rõ khi tô đặc 1 màu.
- [ ] Số màu ≤ bible: `pyxel_validate({maxColors:N, sizeMultipleOf:<grid>})`.
- [ ] `pyxel_analyze`: không còn pixel mồ côi vô ý; màu ngoài palette nằm đúng danh sách hex của bible.
- [ ] Hướng sáng là trên‑trái trên mọi asset; bóng đổ cùng một phía.
- [ ] Không pillow shading, banding, jaggies, double pixel trên outline, mixel.
- [ ] Outline đúng luật của bible (màu/đen, sel‑out, dày 1 px).
- [ ] Kích thước khớp lưới; tỉ lệ nhân vật–tile–prop đúng (cửa cao khoảng 1,5× nhân vật, ghế ngang hông...).
- [ ] Sprite gameplay nổi hơn nền về value; nền ít bão hoà hơn.
- [ ] Đặt cạnh 2–3 asset đã duyệt trước đó: cùng "họ" về độ chi tiết, độ dày nét, độ bão hoà.
- [ ] `mkdir -p` → `export_png` → `save .pyxel`; ghi asset mới vào danh mục trong style bible.

## Lỗi thường gặp và cách sửa
| Lỗi | Dấu hiệu | Sửa |
|---|---|---|
| Pillow shading | tối dần theo vòng từ viền vào tâm | đặt lại nguồn sáng trên‑trái: mặt quay về sáng thì sáng, phía đối diện tối, phần dưới tối nhất |
| Banding | các dải tông chạy song song viền hoặc song song nhau | cho các dải có độ dài khác nhau, so le bậc, gộp bớt tông |
| Quá nhiều màu / ramp thẳng | ảnh "bẩn", xám đục | gộp về 3–4 tông/vật liệu; dùng `pixkit.py ramp` để có hue‑shift |
| Jaggies | đường xiên/cong có bậc 1‑3‑1‑2 lộn xộn | nhịp bậc đều 1‑1, 2‑2 hoặc tăng/giảm dần 1‑2‑3 |
| Double / outline dày | góc chữ L 2 px trên nét 1 px | xoá pixel góc để nét chỉ chạm theo đường chéo |
| Pixel mồ côi | đốm lẻ, nhiễu | `pyxel_ingest({removeOrphans:true})` hoặc `Sprite.clean_orphans()`; chỉ giữ highlight cố ý |
| Mixel | asset khác thang pixel nằm cạnh nhau | vẽ lại đúng grid; không scale 1,5×, không xoay sprite |
| Dither lạm dụng | ảnh rỗ, khó đọc | bỏ dither trên nhân vật; chỉ giữ cho nền hoặc chất liệu ở preset 1‑bit/GB |
| Sprite chìm vào nền | khó thấy nhân vật | tăng value contrast; nền giảm bão hoà; thêm outline hoặc rim light |
| Lệch phong cách | asset mới "lạc loài" | so lại với bible; Shovel Knight đã làm lại King Knight vì chi tiết quá mức |

## Ví dụ 1 — Cây 32×32 theo P1 Cozy Farming (script + import)
Palette (Endesga 32): lá `193c3e 265c42 3e8948 63c74d fee761`, vỏ cây `3e2731 733e39 b86f50 e4a672`.
Ramp đi từ lạnh sang ấm (hue‑shift), phần tử [0] làm outline màu, có sel‑out phía trên‑trái.
```bash
mkdir -p art/props art/out art/src
python3 scripts/pixkit.py tree --out art/props/tree_cozy_32.png   # in ra rows/legend (DB16 gần nhất) + PNG (+ *_x8.png để soi)
```
Chuỗi tool:
1. `pyxel_create_sprite({importPath:"art/props/tree_cozy_32.png", detectNativeRes:false})`
2. `pyxel_preview({mode:"single", scale:12})` → xem cụm lá; nếu highlight vàng quá gắt, chỉnh ramp lá thành `[193c3e,265c42,3e8948,63c74d]` với `tones=3` rồi chạy lại.
3. `pyxel_analyze` → mồ côi = 0 (hoặc chỉ còn highlight cố ý).
4. `pyxel_validate({maxColors:10, sizeMultipleOf:16})` (9 màu + trong suốt; tuỳ cách tool đếm).
5. `pyxel_export_png({path:"art/out/tree_cozy_32.png"})` → `pyxel_save({path:"art/src/tree_cozy_32.pyxel"})`.

## Ví dụ 2 — Hiệp sĩ 16×16 theo P2 NES‑Retro (draw trực tiếp, 5 màu DB16)
Legend: `K`=0 (#000000 outline), `B`=13 (#005784 bóng giáp), `b`=14 (#31a2f2 giáp), `w`=15 (#b2dcef highlight), `Y`=8 (#f7e26b viền vàng). Dấu `.` không có trong legend nên được bỏ qua (giữ trong suốt).
```json
{"rows":[
".....KKKKK......",
"....KbwbbbK.....",
"...KbwbbbbbK....",
"...KbbKKKKKK....",
"...KbbKYKKBK....",
"...KBbbbbbBK....",
"....KBBBBBK.....",
"...KYKbbbKYK....",
"..KbbKbwbbKbK...",
"..KbbKbbbBKbK...",
"..KYYKBBBBKYK...",
"...KKKYYYYKK....",
"....KBBKBBK.....",
"....KbBKbBK.....",
"...KKBBKKBBK....",
"...KKKKKKKKKK..."],
"legend":{"K":0,"B":13,"b":14,"w":15,"Y":8},"mode":"replace"}
```
Chuỗi tool:
1. `pyxel_create_document({width:16, height:16, name:"knight"})`
2. `pyxel_draw(<json trên>)`
3. `pyxel_preview({mode:"single", scale:16})` → kiểm tra highlight `w` nằm phía trái/trên (đúng hướng sáng) và visor đọc được.
4. Chỉnh: ví dụ mở rộng sừng mũ bằng `pyxel_set_pixel({x:4,y:0,color:"fff7e26b"})`; xoá pixel thừa bằng `color:"00000000"`.
5. `pyxel_validate({maxColors:6, sizeMultipleOf:16})` → `mkdir -p art/out art/src` → `pyxel_export_png({path:"art/out/knight.png"})` → `pyxel_save({path:"art/src/knight.pyxel"})`.
6. Walk 4 frame: chép rows, đổi 3 hàng chân (r12–r15) theo pose contact/pass; mỗi frame export `f00..f03.png` rồi ghép ffmpeg như Workflow D.
