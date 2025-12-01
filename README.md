# The Chickening

Một game roguelite action với nhân vật gà con chiến đấu chống đội quân cáo đỏ. Phát triển bằng Python 3.8 và Pygame.

## Cài Đặt
1. Cài Python 3.8 và virtualenv.
2. Chạy `pip install -r requirements.txt`.
3. Chạy game: `python main.py`.

## Cấu Trúc Dự Án
- the_chickening/
- ├── main.py                  `# File chính chạy game, khởi tạo Pygame và loop`
- ├── requirements.txt         `# Danh sách dependencies (pygame==2.1.2, etc.)`
- ├── README.md                `# Tài liệu dự án`
- ├── assets/                  `# Tài nguyên tĩnh`
- │   ├── images/              `# Sprites, backgrounds (e.g., chicken.png, fox.png)`
- │   │   ├── player/
- │   │   ├── enemies/
- │   │   ├── items/
- │   │   └── backgrounds/
- │   └── sounds/              `# Âm thanh (e.g., cluck.wav, auu.wav)`
- ├── data/                    `# Dữ liệu JSON`
- │   ├── items.json           `# Danh sách items và effects`
- │   ├── skills.json          `# Skill tree data`
- │   └── levels.json          `# Cấu trúc màn chơi`
- ├── modules/                 `# Các module chính`
- │   ├── entities/            `# Các thực thể trong game`
- │   │   ├── base_entity.py   `# Class Entity base (position, health, etc.)`
- │   │   ├── player.py        `# Class Player (attacks, dodge, skills)`
- │   │   ├── enemy.py         `# Class Enemy base (AI behaviors)`
- │   │   ├── boss.py          `# Class Boss (phases, special attacks)`
- │   │   ├── projectile.py    `# Đạn (lông, trứng nổ)`
- │   │   └── resource.py      `# Thóc và drops`
- │   ├── managers/            `# Quản lý hệ thống`
- │   │   ├── level_manager.py `# Quản lý waves, spawns, maps`
- │   │   ├── sound_manager.py `# Quản lý nhạc và SFX`
- │   │   └── item_manager.py  `# Quản lý items và synergies`
- │   ├── screens/             `# Các màn hình/game states`
- │   │   ├── main_menu.py     `# Menu chính`
- │   │   ├── game_screen.py   `# Màn chơi chính (arena)`
- │   │   ├── safe_zone.py     `# Chuồng Gà (shop, skills, missions)`
- │   │   └── game_over.py     `# Màn thua`
- │   ├── utils/               `# Công cụ hỗ trợ`
- │   │   ├── constants.py     `# Hằng số (colors, sizes, etc.)`
- │   │   ├── helpers.py       `# Hàm tiện ích (collision, random)`
- │   │   └── hud.py           `# Heads-Up Display (HP, energy bar)`
- │   └── skills.py            `# Hệ thống skills và tree (roguelite)`
- └── tests/                   `# Unit tests (e.g., test_player.py)`


## Tiến Độ
- Ngày 1-4: Setup cơ bản.
- Ngày 5: Viết xong constants.py

Xem `docs/gameplay_design.md` để biết chi tiết gameplay.

## Kế hoạch dự án
- Kế hoạch bao gồm:
- - Giai đoạn 1: Lập kế hoạch và Thiết lập (Ngày 1-20): Xây dựng nền tảng dự án.
- - Giai đoạn 2: Phát triển Core Gameplay (Ngày 21-80): Implement nhân vật, tấn công, di chuyển.
- - Giai đoạn 3: Phát triển Kẻ Thù và Boss (Ngày 81-120): Thêm AI và đối thủ.
- - Giai đoạn 4: Phát triển Hệ Thống Phụ (Ngày 121-160): Items, skills, map, safe zone.
- - Giai đoạn 5: Đồ Họa, Âm Thanh và Polish (Ngày 161-180): Tối ưu hóa trải nghiệm.
- - Giai đoạn 6: Testing và Hoàn Thiện (Ngày 181-200): Kiểm tra và hoàn tất.
- Cụ thể: 
- - Ngày 1: Nghiên cứu và cài đặt môi trường: Cài Python 3.8, Pygame, và các thư viện cần thiết (như pygame.mixer cho âm thanh). Tạo repository Git.
- - Ngày 2: Phân tích gameplay: Viết tài liệu chi tiết về các tính năng chính (nhân vật, kẻ thù, boss) dựa trên mô tả của bạn.
- - Ngày 3: Thiết kế UML diagram cho các class chính (Player, Enemy, Item) bằng công cụ như Draw.io.
- - Ngày 4: Tạo thư mục dự án cơ bản (main.py, assets/, modules/).
- - Ngày 5: Viết constants.py trong utils/ để định nghĩa hằng số (màu sắc, kích thước màn hình, HP mặc định).
- - Ngày 6: Thiết lập main.py: Khởi tạo window Pygame cơ bản và loop chính.
- - Ngày 7: Thêm FPS counter và basic event handling trong main.py.
- - Ngày 8: Tạo module screens/: Viết game_screen.py với hàm draw background đơn giản.
- - Ngày 9: Tích hợp asset loading: Tạo assets/images/ và load một sprite test (gà con).
- - Ngày 10: Test run dự án cơ bản: Chạy main.py để hiển thị window với background.
- - Ngày 11: Viết helpers.py trong utils/ cho các hàm tiện ích (collision detection).
- - Ngày 12: Thiết kế database đơn giản (JSON) cho items và skills trong data/.
- - Ngày 13: Tạo module entities/: Viết base_entity.py cho class Entity chung.
- - Ngày 14: Kiểm tra và debug lỗi cơ bản trong setup.
- - Ngày 15: Viết tài liệu README.md cho dự án.
- - Ngày 16: Thiết kế level structure: Viết level_manager.py trong managers/.
- - Ngày 17: Thêm sound manager cơ bản trong managers/sound_manager.py.
- - Ngày 18: Tạo assets/sounds/ và load sound test.
- - Ngày 19: Commit Git và review giai đoạn 1.
- - Ngày 20: Buffer: Sửa lỗi hoặc nghiên cứu Pygame thêm nếu cần.
- - Ngày 21: Implement class Player trong entities/player.py: Thêm vị trí, di chuyển cơ bản (WASD).
- - Ngày 22: Thêm thanh HP cho Player và hiển thị HUD trong hud.py.
- - Ngày 23: Implement dodge roll cho Player: Thêm cooldown và animation cơ bản.
- - Ngày 24: Thêm tấn công gần (mổ): Logic sát thương và hitbox.
- - Ngày 25: Thêm tấn công xa (bắn lông): Sử dụng Eggnergy, projectile class trong entities/projectile.py.
- - Ngày 26: Thêm tấn công trứng nổ: Limit số lượng, explosion effect.
- - Ngày 27: Test player movement và attacks trong game_screen.py.
- - Ngày 28: Thêm energy bar (Eggnergy) cho Player.
- - Ngày 29: Implement skill system cơ bản trong skills.py: Class Skill base.
- - Ngày 30: Kết nối Player với skills: Mở khóa skill đầu tiên.
- - Ngày 31: Thêm thu thập thóc: Class Resource trong entities/resource.py.
- - Ngày 32: Logic mất thóc khi chết: Save/load thóc ở safe zone.
- - Ngày 33: Thiết kế safe zone (Chuồng Gà) trong screens/safe_zone.py.
- - Ngày 34: Implement hồi máu ở safe zone.
- - Ngày 35: Thêm shop trong safe_zone.py: Menu mua items.
- - Ngày 36: Implement skill tree: Random 3 skills mỗi lần nâng cấp.
- - Ngày 37: Thêm mission board: Nhiệm vụ đơn giản (kill X enemies).
- - Ngày 38: Nâng cấp chuồng: Logic giảm giá shop.
- - Ngày 39: Test safe zone integration.
- - Ngày 40: Buffer: Debug player và safe zone.
- - Ngày 41-50: Phát triển 3 nhánh skill tree (Chiến binh, Xạ thủ, Bom thủ): Mỗi ngày một nhánh, thêm 3-5 skills.
- - Ngày 51: Kết nối skill tree với Player.
- - Ngày 52: Thêm hiệu ứng hiệp lực items (synergy).
- - Ngày 53: Implement item system trong items.py: Class Item với rarity.
- - Ngày 54: Thêm ví dụ items (Mỏ thép, Bộ lông thép).
- - Ngày 55: Equip items cho Player.
- - Ngày 56: Test item effects trên attacks.
- - Ngày 57: Thêm map cơ bản: Wave-based arena trong level_manager.py.
- - Ngày 58: Spawn points cho enemies.
- - Ngày 59: Logic qua màn: Phá spawn points.
- - Ngày 60: Test core gameplay loop.
- - Ngày 61-70: Buffer và refine player mechanics (tăng tốc độ, sát thương theo items).
- - Ngày 71-80: Tối ưu hóa performance: Thêm quadtree cho collision nếu cần.
- - Ngày 81: Implement base Enemy trong entities/enemy.py.
- - Ngày 82: Thêm Cáo chạy nhanh: AI áp sát zig-zag.
- - Ngày 83: Thêm Cáo cung thủ: Giữ khoảng cách, né.
- - Ngày 84: Thêm Cáo ném bom: Tấn công diện rộng.
- - Ngày 85: Thêm Cáo giáp: Điểm yếu phía sau.
- - Ngày 86: Thêm Cáo pháp sư: Buff và vòng cản.
- - Ngày 87: Test enemy AI cơ bản.
- - Ngày 88: Thêm drop thóc từ enemies.
- - Ngày 89: Implement Boss base trong entities/boss.py.
- - Ngày 90: Boss 1 (Cáo Đại Tướng): Thương dài, lao.
- - Ngày 91: Thêm pha biến đổi cho Boss (3 pha).
- - Ngày 92: Spawn đàn cáo con ở 50% HP.
- - Ngày 93: Test boss fight.
- - Ngày 94: Tăng độ khó: Tốc độ enemies tăng theo wave.
- - Ngày 95: Boss học né: Adaptive AI đơn giản.
- - Ngày 96: Thêm đa dạng enemies theo wave.
- - Ngày 97: Integrate enemies vào level_manager.py.
- - Ngày 98: Test wave system.
- - Ngày 99: Buffer: Debug AI errors.
- - Ngày 100-110: Phát triển thêm boss cho màn sau (tương tự Boss 1, mỗi ngày một boss).
- - Ngày 111-120: Tích hợp boss mỗi 5 màn, test full level.
- - Ngày 121: Thêm môi trường map: Trang trại, rừng (background layers).
- - Ngày 122: Interactable objects (hũ, bụi rậm drop thóc).
- - Ngày 123: Logic rủi ro-thưởng: Mất thóc khi chết.
- - Ngày 124: Main menu trong screens/main_menu.py.
- - Ngày 125: Game over screen.
- - Ngày 126: Save/load game state (JSON).
- - Ngày 127: Implement Game+ mode: Khó hơn, skin mới.
- - Ngày 128: Thêm Đại Trùm Cáo Chúa ở màn cuối.
- - Ngày 129: Test endgame.
- - Ngày 130: Buffer: Refine systems.
- - Ngày 131-140: Thêm items và skills còn lại (mỗi ngày 2-3 items).
- - Ngày 141-150: Tích hợp synergy effects.
- - Ngày 151-160: Tối ưu hóa roguelite elements (random skills).
- - Ngày 161: Chuyển sang pixel art: Load sprites cho player, enemies.
- - Ngày 162: Animation cho attacks và dodge.
- - Ngày 163: Hiệu ứng lông văng thay máu.
- - Ngày 164: Background music theo wave.
- - Ngày 165: SFX: "Cục cục!", "Auu!".
- - Ngày 166: Test audio integration.
- - Ngày 167-170: Polish UI (HUD, menus).
- - Ngày 171-175: Thêm oblique projection view.
- - Ngày 176-180: Optimize graphics performance.
- - Ngày 181-190: Unit tests cho modules (player, enemy, etc.).
- - Ngày 191-195: Playtesting: Chơi qua full game, fix bugs.
- - Ngày 196: Build executable (pyinstaller).
- - Ngày 197: Documentation cuối cùng.
- - Ngày 198: Commit final Git.
- - Ngày 199: Buffer cho bất kỳ sửa chữa cuối.
- - Ngày 200: Hoàn thành: Release version 1.0.