# Cơ sở nghiên cứu phong cách pixel art game

Tài liệu nền cho các nguyên tắc trong `SKILL.md`. Mức độ tin cậy được ghi rõ; mục đánh dấu (*) là quan sát phổ biến trong cộng đồng, chưa có nguồn chính thức.

## 1. Quy trình chuyên nghiệp

**Giới hạn màu & mảng phẳng.** Pedro Medeiros (Saint11 — Celeste, TowerFall) khuyên giữ số màu thấp (dưới 32), để mảng lớn màu phẳng cho mắt nghỉ, và đơn giản hoá thiết kế khi một vùng nhỏ bị nhồi quá nhiều chi tiết. Khối hộp dễ vẽ hơn hình trụ/tròn. Silhouette nói lên vật thể; phần trong giữ ít chi tiết. Dither dùng dè dặt.

**Độ phân giải thấp = giải đố.** Mỗi pixel là một mảnh ghép phải mang nghĩa. Chuyển concept sang sprite là chọn cái gì hiện, cái gì để người xem tự tưởng tượng (ví dụ Theo trong Celeste giữ râu/tóc/khăn/ba lô; tư thế thả lỏng chỉ là lùi thân 1 px). Ưu tiên góc 90°; bỏ outline ở nhiều chỗ; tránh dither trên quần áo (có ngoại lệ chủ đích).

**Ramp màu & hue shifting (Slynyrd, Pixelblog #1).** Ramp tốt phải hue‑shift, không phải "straight ramp" chỉ đổi sáng/bão hoà. Palette mẫu dịch hue +20° mỗi bước; "20 is about as high as I go". Độ sáng tăng đều trái→phải, thường không bắt đầu từ 0; bão hoà đỉnh ở giữa ramp, không chạm 100 hay 0. Highlight ngả vàng, bóng ngả lam/tím.

**Lỗi kinh điển (androidarts, Pixel Joint):** pillow shading (tối dần theo vòng vào tâm — sửa bằng bám hướng sáng); banding (dải tông song song — cho dải lệch độ dài, so le bậc); jaggies (bậc đường không đều — giữ nhịp 2‑2 hoặc 1‑2‑3); nhiễu/pixel mồ côi (do nhồi chi tiết); dither lạm dụng. Pixel mồ côi vẫn dùng được có chủ đích (tia lấp lánh 1 px).

**Pipeline 3D→pixel (Dead Cells, Motion Twin).** Dựng model 3D từ model sheet pixel 2D, xuất mỗi frame ra PNG kèm normal map, toon shader lên khối, rồi "pixelate". Nhân vật ~50 px nên đầu tư 3D quá nhiều là kém hiệu quả.

## 2. Giữ đồng bộ phong cách

- **Giới hạn chung cho cả cast.** Yacht Club (Shovel Knight) cho mỗi nhân vật "4‑5 colors + transparency". Bản King Knight đầu quá chi tiết ("gần 16‑bit hơn") bị làm lại. Quá nhiều màu → lạc lõng; quá chi tiết → khó animate.
- **Cố định kích thước theo lưới.** ConcernedApe: tile 16×16 giúp khối lượng art Stardew "manageable". Item/tile 16×16, NPC ngoài map 16×32, chân dung 64×64.
- **Cùng một thang pixel.** Hyper Light Drifter khoá nội suy 480×270 (1/4 của 1080p). Không trộn mixel, không xoay/scale lẻ.
- **Hiệu ứng thống nhất che bất đồng.** Katana ZERO phủ "cohesive neon glow" nên các asset lệch phong cách từ nhiều artist vẫn trông đồng bộ.

## 3. Phong cách game nổi tiếng (tóm tắt)

| Game | Dữ kiện có nguồn | Đặc trưng áp dụng |
|---|---|---|
| Stardew Valley | Tile 16×16, NPC 16×32, chân dung 64×64 | Ấm, bão hoà vừa, outline sẫm có màu (*), 3–4 tông, top‑down 3/4 |
| Celeste | Chọn chi tiết có nghĩa, ưu tiên 90°, bỏ outline nhiều chỗ, tránh dither trên áo | Nhân vật rất nhỏ, mảng phẳng, palette theo cảm xúc màn |
| Shovel Knight | Palette NES; mỗi nhân vật 4–5 màu + trong suốt; thêm vài màu tối/giảm bão hoà | Outline đen, khối phẳng, bão hoà cao, NES "trong ký ức" |
| Hyper Light Drifter | 480×270; "bright, saturated, neon, muted" | Neon/pastel trên nền tối, ít outline (*) |
| Dead Cells | 3D→pixel, nhân vật ~50 px, toon + normal map | Animation mượt nhiều frame, tương phản mạnh |
| Sea of Stars / Octopath | Kế thừa SNES JRPG; Octopath HD‑2D (sprite 2D trong môi trường 3D) | Sprite SNES + DOF/bloom, mật độ pixel cao hơn SNES |
| Blasphemous | "Purist", không shader/3D, tinh thần Neo Geo | Gothic Tây Ban Nha, tối, ít bão hoà, nhấn đỏ máu (*) |
| Owlboy / Eastward | "Hi‑bit", painterly, nhiều màu, AA tinh; Eastward dựng bằng Aseprite | Chi tiết dày, ánh sáng điện ảnh |
| Katana ZERO | Neon glow thống nhất | Nền tối, neon tím/hồng/cyan |
| Enter the Gungeon | "200,000+ sprites" vẽ tay; Bulletkin định hướng art | Outline đen dày, "đồ vật có mắt", đạn dễ đọc |
| Minit / Downwell | Minit 1‑bit trắng đen; Downwell palette 4 màu (đỏ = nguy hiểm/gem, lam = nước) | 1–4 màu; màu nhấn mang nghĩa gameplay |

## Caveats
- Mâu thuẫn nguồn Shovel Knight: thêm 4 hay 5 màu ngoài NES — skill chỉ dùng điểm chung "gần như toàn NES + vài màu tối/giảm bão hoà".
- Downwell: nhiều nguồn nói 3 hoặc 4 màu; hex "Downwell Vivid" là bản fan trên Lospec, không phải giá trị chính thức.
- Chưa xác minh bằng nguồn chính: độ phân giải nội Downwell/Minit, thang pixel Owlboy, kích thước sprite Katana ZERO / Enter the Gungeon, palette Kingdom. Số frame animation và bộ autotile 16/47 là quy ước cộng đồng — coi là điểm khởi đầu.
- AAP‑64 lấy từ snapshot tìm kiếm → đối chiếu lại trên Lospec.
- Hành vi MCP chưa kiểm chứng đầy đủ: cách `pyxel_validate` đếm `maxColors` (có tính trong suốt không), `create_sprite(importPath)` có giữ nguyên màu ngoài DB16 không, danh sách tool mà `batch` chấp nhận. → Luôn kiểm tra bằng `pyxel_analyze` và `dry_run`.

## Nguồn chính
- Saint11 — Pixel Art Fundamentals 1 (patreon.com/saint11)
- Saint11 — My Thoughts on Very Low Resolution (teamkano.medium.com)
- Slynyrd — Pixelblog #1: Color Palettes (slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes)
- the-pixel.art — Hue Shifting; Clusters/Orphan Pixels/Banding
- androidarts.com/pixtut — Pixel Art Tutorial WIP; Pixel Joint — The Pixel Art Tutorial
- Yacht Club / David D'Angelo — "Breaking the NES" (Engadget); Nick Wozniak
- Gamasutra/Game Developer — Hyper Light Drifter (Road to IGF); Dead Cells 3D pipeline; Eastward; Kingdom Two Crowns
- Lospec palette list — DawnBringer 32, Endesga 32, Sweetie 16, SLSO8, Resurrect 64, AAP‑64, hept32, Arq4, Original Gameboy, NES, Downwell Vivid
- ConcernedApe interview (mentalnerd.com); Stardew modding forum (sprite sizes)
