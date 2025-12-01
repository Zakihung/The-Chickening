# The Chickening – Gameplay Design Document

## 1. Giới Thiệu Tổng Quan
- **Thể loại**: Roguelite Action Arena (wave-based survival với elements risk-reward).
- **Góc nhìn**: Pixel art angled top-down / oblique projection.
- **Mục tiêu**: Sống sót qua các màn, đánh bại Đại Trùm Cáo Chúa, mở Game+.
- **Cơ chế cốt lõi**: Di chuyển né tránh, 3 loại tấn công, thu thập thóc (rủi ro mất khi chết), nâng cấp ở safe zone.

## 2. Nhân Vật Chính: Gà Con (Player)
- **Thuộc tính cơ bản** (có thể nâng cấp qua items/skills):
  | Thuộc tính     | Giá trị mặc định | Mô tả |
  |----------------|------------------|-------|
  | HP             | 100              | Thanh máu, hồi dần ở safe zone. |
  | Tốc độ di chuyển | 5 pixels/frame | Tăng/giảm qua items (ví dụ: Giày Phụt Lông +2). |
  | Sát thương cơ bản | 10              | Áp dụng cho tất cả attacks. |
  | Eggnergy (năng lượng) | 50/50       | Dùng cho bắn lông, hồi dần theo thời gian. |

- **Kỹ năng di chuyển**:
  - **Dodge Roll**: Lăn né (phím Shift), invincible 0.5s, cooldown 1s, di chuyển xa 100 pixels.

- **Ba loại tấn công chính** (phím chuột trái/giữ/phải, hoặc Q/E/R):
  | Tấn công       | Phím     | Tầm    | Sát thương | Cooldown/Chi phí | Mô tả |
  |----------------|----------|--------|------------|------------------|-------|
  | Mổ tầm gần    | Left Click | 50px  | 10-15     | 0.3s            | Tốc độ nhanh, hitbox nhỏ phía trước. |
  | Bắn lông tầm xa | Hold Left | 300px | 20        | 10 Eggnergy/đạn | Projectile bay thẳng, pierce 1 enemy. |
  | Đẻ trứng nổ   | Right Click | 200px | 50 (AoE 100px) | 1 quả/10s      | Ném trứng, nổ sau 1s, limit 3 quả max. |

- **Kỹ năng chủ động/bị động**: Mở khóa qua skill tree (xem phần 8).

## 3. Kẻ Thù: Đội Quân Cáo Đỏ
- **Thuộc tính chung**: HP 50-200, drop thóc 1-5 khi chết, AI dựa trên state machine (idle, chase, attack, flee).
- **Các loại cáo** (tăng dần theo màn):

  | Loại          | HP   | Tốc độ | Vũ khí/Kỹ năng          | Hành vi AI (Pathfinding: A* đơn giản hoặc vector-based) |
  |---------------|------|--------|-------------------------|-------------------------------------------------------|
  | Cáo chạy nhanh | 50  | 7     | Vuốt cào (sát thương 15)| Zig-zag áp sát player, tấn công khi <50px.           |
  | Cáo cung thủ  | 70  | 4     | Bắn tên (20 dmg, 200px)| Giữ khoảng cách 150-250px, né dodge nếu player gần.  |
  | Cáo ném bom   | 80  | 5     | Bom khoai tây (AoE 30 dmg)| Ném bom tạo vùng nguy hiểm 2s, chạy xa sau ném.      |
  | Cáo giáp      | 150 | 3     | Khiên gỗ (block front) | Chỉ nhận dmg từ phía sau (rotate chậm).              |
  | Cáo pháp sư   | 60  | 4     | Lửa (DoT 5/s) + Triệu hồi | Buff tốc độ đồng đội +20%, tạo vòng lửa cản đường.    |

- **Spawn**: Từ spawn points (phá được, HP 100), số lượng tăng theo wave.

## 4. Trùm Cáo Đỏ (Boss)
- **Xuất hiện**: Mỗi 5 màn, màn riêng lớn hơn.
- **Thuộc tính chung**: HP 1000-5000, 3 pha (mất 33% HP mỗi pha: tăng tốc +20%, unlock skill mới).
- **Ví dụ Boss 1: Cáo Đại Tướng**
  | Pha | HP còn | Kỹ năng mới |
  |-----|--------|-------------|
  | 1   | 100-67%| Thương dài (reach 150px, dmg 30). |
  | 2   | 66-34%| Lao về player (dash 300px, dmg 40). |
  | 3   | <33%  | Tạo đàn cáo con (5 con nhỏ, HP 20 mỗi). |

- **AI nâng cao**: Học pattern player (nếu dodge quá nhiều, boss predict vị trí roll).

## 5. Các Tính Năng Khác (Tóm tắt để reference sau)
- **Thu thập thóc**: Drop từ quái/hũ, lưu ở safe zone, mất 50% nếu chết.
- **Safe Zone (Chuồng Gà)**: Shop, Skill Tree (random 3 chọn 1), Mission Board.
- **Skill Tree**: 3 nhánh (Mỏ Sắt, Xạ Lông, Trứng Nổ).
- **Items**: Rarity Common-Legendary, synergy (ví dụ: Lông cháy + Trứng xăng = burn lâu hơn).
- **Map**: Wave 5-10, môi trường thay đổi (trang trại → núi lửa).

Tài liệu này sẽ được cập nhật liên tục khi code.