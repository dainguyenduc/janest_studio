# Style presets (P1–P11) + palette hex

## Bảng preset

| # | Preset | Game tham chiếu | Tile / nhân vật | Palette | Outline | Shading / dither | Cảm xúc → thể loại |
|---|---|---|---|---|---|---|---|
| P1 | **Cozy Farming** | Stardew Valley | Tile 16, nhân vật 16×32, item 16×16, chân dung 64×64 | Endesga 32 (ấm) hoặc Resurrect 64 | Có màu, lấy tông tối nhất của ramp vật liệu; sel‑out phía sáng | 3–4 tông, hue‑shift ấm khi sáng lên; không dither | Ấm áp, thư thái → farming sim, life sim, cozy RPG |
| P2 | **NES‑Retro** | Shovel Knight, Mega Man | Tile 16 (meta 8×8), nhân vật 16×16 đến 32×32 | NES 55, mỗi sprite 3 màu + trong suốt (Shovel Knight nới lên 5) | Đen `000000` 1 px | Phẳng 2–3 tông, không AA, dither checker thưa cho nền | Hoài cổ, gắt → platformer, action |
| P3 | **Game Boy 2‑bit** | Pokémon Red/Blue, Link's Awakening | Tile 8×8, nhân vật 16×16 | GB Original 4 màu | Tông tối nhất | 4 tông; dither checker được phép | Hoài niệm, tối giản → game jam, puzzle, RPG nhỏ |
| P4 | **PICO‑8 Lo‑fi** | game PICO‑8, Celeste Classic | Sprite 8×8, màn hình 128×128 | PICO‑8 16 | Tuỳ, thường không có | 1–2 tông, ký hiệu hoá | Vui, gọn → jam, arcade, roguelike nhỏ |
| P5 | **SNES JRPG** | Chrono Trigger, FF6, Sea of Stars, Octopath | Tile 16, nhân vật 16×24 đến 24×32, tỉ lệ chibi 2–3 đầu | DawnBringer 32 | Có màu sẫm, sel‑out | 4–5 tông, hue‑shift, AA chọn lọc | Phiêu lưu, sử thi → JRPG, tactics |
| P6 | **Moody Atmospheric** | Hyper Light Drifter, Celeste | Màn hình 480×270 hoặc 320×180, nhân vật nhỏ 16–32 | SLSO8 hoặc Sweetie 16, mỗi khu vực 1 bảng giới hạn | Ít hoặc không có; tách bằng tương phản value | Mảng phẳng lớn, 2–3 tông; gradient/dither có chủ đích cho bầu trời | Cô độc, mơ màng → action‑adventure, platformer cảm xúc |
| P7 | **Gritty Dark Fantasy** | Blasphemous, Dead Cells | Nhân vật 48–64 px trở lên, tile 16 hoặc 32 | Resurrect 64 hoặc AAP‑64, giảm bão hoà, 1 màu nhấn đỏ | Sẫm, gần đen nhưng có màu | 4–6 tông, tương phản mạnh, rim light; animation nhiều frame | Nặng nề, tôn giáo → metroidvania, soulslike, horror |
| P8 | **Minimal 1‑bit/2‑bit** | Minit, Downwell | Nhân vật 8–16, tile 8 hoặc 16 | 2 màu `000000/ffffff`, hoặc 4 màu kiểu Downwell, hoặc Arq4 | Không có, hoặc nền là outline | Không đổ bóng; dither 1‑bit cho chất liệu; một màu nhấn mang nghĩa gameplay | Sắc, khó → roguelike nhanh, puzzle, game ngắn |
| P9 | **Neon Action** | Katana ZERO | Nhân vật 32–48, tile 16 | hept32, hoặc Endesga 32 với nền `181425/262b44` | Không có; glow 1 px màu sáng | Rim light neon, tương phản cực cao | Căng, điện ảnh → action, stealth, cyberpunk |
| P10 | **Arcade Bullet‑hell / Roguelike** | Enter the Gungeon | Nhân vật 16–24, đạn 4–8 px, tile 16 | Sweetie 16 hoặc PICO‑8; đạn dùng màu riêng không xuất hiện ở nền | Đen dày 1 px | 2–3 tông, khối tròn bầu, dễ đọc ở 1× | Vui, hỗn loạn → shmup, twin‑stick, roguelike |
| P11 | **Hi‑bit Painterly** | Owlboy, Eastward | Nhân vật 24–48, tile 16–32 | AAP‑64 hoặc Resurrect 64 | Có màu, chọn lọc | 5–7 tông, AA tinh, ánh sáng điện ảnh, hạn chế dither | Phong phú, ấm → adventure, metroidvania, narrative |

## Palette hex (xác minh trên Lospec, trừ chỗ ghi chú)

- **DB16** (palette mặc định của MCP pixel-art): `000000 ffffff 9d9d9d be2633 e06f8b 493c2b a46422 eb8931 f7e26b 2f484e 44891a a3ce27 1b2632 005784 31a2f2 b2dcef`
- **DawnBringer 32**: `000000 222034 45283c 663931 8f563b df7126 d9a066 eec39a fbf236 99e550 6abe30 37946e 4b692f 524b24 323c39 3f3f74 306082 5b6ee1 639bff 5fcde4 cbdbfc ffffff 9badb7 847e87 696a6a 595652 76428a ac3232 d95763 d77bba 8f974a 8a6f30`
- **Endesga 32**: `be4a2f d77643 ead4aa e4a672 b86f50 733e39 3e2731 a22633 e43b44 f77622 feae34 fee761 63c74d 3e8948 265c42 193c3e 124e89 0099db 2ce8f5 ffffff c0cbdc 8b9bb4 5a6988 3a4466 262b44 181425 ff0044 68386c b55088 f6757a e8b796 c28569`
- **PICO‑8**: `000000 1d2b53 7e2553 008751 ab5236 5f574f c2c3c7 fff1e8 ff004d ffa300 ffec27 00e436 29adff 83769c ff77a8 ffccaa`
- **Sweetie 16** (GrafxKid): `1a1c2c 5d275d b13e53 ef7d57 ffcd75 a7f070 38b764 257179 29366f 3b5dc9 41a6f6 73eff7 f4f4f4 94b0c2 566c86 333c57`
- **SLSO8** (Luis Miguel Maldonado): `0d2b45 203c56 544e68 8d697a d08159 ffaa5e ffd4a3 ffecd6`
- **Game Boy "Original"**: `0f380f 306230 8bac0f 9bbc0f`; biến thể bgb: `081820 346856 88c070 e0f8d0`
- **Arq4** (ENDESGA): `ffffff 6772a9 3a3277 000000`
- **Downwell Vivid** (palette do fan gửi lên Lospec — không phải giá trị chính thức của game): `fef6fe c90000 496ab4 003046`
- **hept32** (ENDESGA, kế nhiệm EDG32, tương phản/bão hoà cao hơn): `000000 180d2f 353658 686b72 8b97b6 c5cddb ffffff 5ee9e9 2890dc 1831a7 053239 005f41 08b23b 47f641 e8ff75 fbbe82 de9751 b66831 8a4926 461c14 1e090d 720d0d 813704 da2424 ef6e10 ecab11 ece910 f78d8d f94e6d c12458 841252 3d083b`
- **Resurrect 64** (Kerrie Lake): `2e222f 3e3546 625565 966c6c ab947a 694f62 7f708a 9babb2 c7dcd0 ffffff 6e2727 b33831 ea4f36 f57d4a ae2334 e83b3b fb6b1d f79617 f9c22b 7a3045 9e4539 cd683d e6904e fbb954 4c3e24 676633 a2a947 d5e04b fbff86 165a4c 239063 1ebc73 91db69 cddf6c 313638 374e4a 547e64 92a984 b2ba90 0b5e65 0b8a8f 0eaf9b 30e1b9 8ff8e2 323353 484a77 4d65b4 4d9be6 8fd3ff 45293f 6b3e75 905ea9 a884f3 eaaded 753c54 a24b6f cf657f ed8099 831c5d c32454 f04f78 f68181 fca790 fdcbb0`
- **AAP‑64** (Adigun A. Polack; đối chiếu lại trên Lospec khi dùng): `060608 141013 3b1725 73172d b4202a df3e23 fa6a0a f9a31b ffd541 fffc40 d6f264 9cdb43 59c135 14a02e 1a7a3e 24523b 122020 143464 285cc4 249fde 20d6c7 a6fcdb ffffff fef3c0 fad6b8 f5a097 e86a73 bc4a9b 793a80 403353 242234 221c1a 322b28 71413b bb7547 dba463 f4d29c dae0ea b3b9d1 8b93af 6d758d 4a5462 333941 422433 5b3138 8e5252 ba756a e9b5a3 e3e6ff b9bffb 849be4 588dbe 477d85 23674e 328464 5daf8d 92dcba cdf7e2 e4d2aa c7b08b a08662 796755 5a4e44 423934`
- **NES** (bản 55 màu trên Lospec; không có một palette NES "chuẩn" duy nhất): `000000 fcfcfc f8f8f8 bcbcbc 7c7c7c a4e4fc 3cbcfc 0078f8 0000fc b8b8f8 6888fc 0058f8 0000bc d8b8f8 9878f8 6844fc 4428bc f8b8f8 f878f8 d800cc 940084 f8a4c0 f85898 e40058 a80020 f0d0b0 f87858 f83800 a81000 fce0a8 fca044 e45c10 881400 f8d878 f8b800 ac7c00 503000 d8f878 b8f818 00b800 007800 b8f8b8 58d854 00a800 006800 b8f8d8 58f898 00a844 005800 00fcfc 00e8d8 008888 004058 f8d8f8 787878`

## Ramp gợi ý sẵn (tối → sáng; phần tử [0] = outline màu)

- **P1 Endesga32** — leaf `193c3e 265c42 3e8948 63c74d fee761` | bark `3e2731 733e39 b86f50 e4a672` | skin `733e39 c28569 e8b796` | water `262b44 124e89 0099db 2ce8f5` | stone `262b44 3a4466 5a6988 8b9bb4 c0cbdc`
- **P5 DB32** — grass `323c39 4b692f 6abe30 99e550` | wood `45283c 663931 8f563b d9a066` | sky `3f3f74 306082 639bff cbdbfc`
- **P6 SLSO8** — cả 8 màu là 1 ramp đêm→bình minh: `0d2b45 203c56 544e68 8d697a d08159 ffaa5e ffd4a3 ffecd6`
- **P7 Resurrect64** — blood `6e2727 b33831 ea4f36` | stone `2e222f 3e3546 625565 7f708a 9babb2` | gold `7a3045 9e4539 cd683d e6904e fbb954`
- **P3 GB** — `0f380f 306230 8bac0f 9bbc0f` (cả game chỉ 4 màu)
- **P8 1‑bit** — `000000 ffffff`; màu nhấn `c90000` (nguy hiểm / vật phẩm thu thập)

> Mẹo: dựng ramp mới nhanh bằng `python3 scripts/pixkit.py ramp --base <hex> --n 5` (tự hue‑shift, bão hoà đỉnh ở giữa).
