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
- │   │   │    ├── player/chicken.png
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
- │   │   ├── base_entity.py   `# Class base cho entities (position, HP, update với di chuyển delta_time, draw với HP bar)`
- │   │   ├── player.py        `# Class Player (movement input handling, flip sprite, dodge placeholder)`
- │   │   ├── enemy.py         `# Class Enemy base (AI random, zig-zag áp sát cho 'runner', collision damage)`
- │   │   ├── boss.py          `# Class Boss (phases, special attacks)`
- │   │   ├── projectile.py    `# Class Projectile (movement, explode, collision/damage handling)`
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
- Ngày 5: Thêm constants.py (các hằng số thiết yếu dựa trên gameplay (có thể mở rộng sau))
- Ngày 6: Khởi tạo Pygame, thiết lập window, và loop chính với event handling cơ bản:
  - Import thêm COLOR_WHITE từ constants (thêm vào constants.py nếu chưa: COLOR_WHITE = (255, 255, 255)). 
  - Thêm xử lý KEYDOWN cho ESC để quit (dễ test).
  - Thêm text đơn giản để window không trống, dễ kiểm tra font hoạt động.
  - Cấu trúc loop chuẩn: Events -> Update -> Draw -> Flip -> Tick.
- Ngày 7: Thêm FPS counter (hiển thị frames per second để debug performance) và basic event handling (xử lý sự kiện như nhấn phím để test tương tác)
  - Import thêm COLOR_RED từ constants (thêm vào constants.py nếu chưa: COLOR_RED = (255, 0, 0)).
  - Thêm biến background_color để test input.
  - Event KEYDOWN cho SPACE: Thay đổi màu nền (đen <-> đỏ) để thấy input hoạt động.
  - FPS counter: Sử dụng clock.get_fps() và blit text ở (10, 10).
- Ngày 8: Tạo module screens/ trong modules/, và viết file game_screen.py với hàm draw background đơn giản:
  - Class GameScreen nhận screen từ Pygame.
  - draw_background: Fill màu xanh (thêm COLOR_GREEN = (0, 255, 0) vào constants.py nếu chưa).
  - Thêm rect đơn giản để test vẽ.
- Ngày 9: Tích Hợp asset loading bằng cách tạo đầy đủ thư mục assets/images/, tải/load một sprite test (hình gà con pixel art), và hiển thị nó trên màn hình để test.
- Ngày 10: Test run dự án cơ bản bằng cách chạy main.py để đảm bảo window hiển thị đúng với background, text, FPS, event handling, và sprite.
- Ngày 11: Viết file helpers.py trong modules/utils/ chứa các hàm tiện ích chung, tập trung vào collision detection (kiểm tra va chạm giữa Rects và circles – dùng cho attacks, enemies sau). Các hàm khác như distance, clamp (giới hạn vị trí), lerp (smooth interpolation) để hỗ trợ movement.
  - rect_collision: Dùng Rect.colliderect() của Pygame (nhanh).
  - circle_collision: Cho explosion AoE hoặc hitbox tròn.
  - Các hàm khác: Cơ bản cho AI, movement.
- Ngày 12: Thiết kế database đơn giản sử dụng file JSON cho items và skills trong thư mục data/. Điều này sẽ lưu trữ dữ liệu tĩnh cho items (trang bị với hiệu ứng, độ hiếm, synergies) và skills (skill tree với branches, random upgrades theo roguelite). Sử dụng JSON vì dễ đọc, không cần database phức tạp, và dễ load vào Python sau (sử dụng json module).
- Ngày 13: Thiết kế file levels.json trong thư mục data/ để định nghĩa cấu trúc màn chơi (levels). File này sẽ lưu trữ dữ liệu tĩnh cho các màn, bao gồm số wave mỗi level, loại kẻ thù spawn theo wave, điểm spawn (có thể phá hủy), boss ở mỗi 5 level, và môi trường (background/map như trang trại, rừng, v.v.). Sử dụng JSON để dễ load sau (trong level_manager.py).
- Ngày 14: Tạo file base_entity.py trong thư mục modules/entities/ để định nghĩa class Entity cơ bản. Đây là class base cho tất cả thực thể trong game (như player, enemies, boss, projectiles), bao gồm thuộc tính cơ bản như vị trí (position), sức khỏe (health/HP), và methods đơn giản như update() và draw() placeholder.
  - Sử dụng pygame.Rect cho position (dễ collision với helpers.py).
  - HP và speed từ constants.py (import để dùng default).
  - Methods cơ bản: update (cho logic), draw (cho render), take_damage (cho combat), is_colliding_with (dùng helpers).
  - Placeholder cho image (sẽ load sprite thực sau).
- Ngày 15: Thêm chi tiết hơn cho methods update() và draw() trong base_entity.py. Chúng ta sẽ refine update để bao gồm di chuyển cơ bản (dựa trên speed và direction placeholder), check chết, và delta_time cho mượt mà; draw sẽ thêm vẽ HP bar đơn giản (thanh máu) và hỗ trợ load image nếu có.
  - Thêm self.direction = pygame.Vector2(0, 0) cho di chuyển (subclass sẽ set direction dựa trên input/AI).
  - Update: Thêm di chuyển với delta_time (mượt mà, không phụ thuộc FPS), clamp để không ra ngoài màn.
  - Draw: Thêm HP bar (thanh máu) đơn giản trên đầu entity, dùng colors từ constants.
  - Import thêm COLOR_RED, COLOR_GREEN, COLOR_BLACK và SCREEN_WIDTH, SCREEN_HEIGHT từ constants.
- Ngày 16: Tạo file player.py trong modules/entities/ để định nghĩa class Player kế thừa từ BaseEntity. Chúng ta sẽ thêm thuộc tính cụ thể cho gà con như HP mặc định, speed từ constants, và placeholder cho attacks/dodge (sẽ chi tiết sau).
  - Kế thừa BaseEntity, set vị trí giữa màn, load chicken.png và scale.
  - Thêm eggnergy, damages từ gameplay.
  - Update: Thêm param keys cho input, set direction dựa WASD/arrows.
  - Draw: Thêm eggnergy bar (vàng) dưới HP bar.
- Ngày 17: Thêm input handling chi tiết hơn cho player movement trong player.py. Chúng ta sẽ refine update() để xử lý input mượt mà (WASD/arrows cho di chuyển, normalize direction để tốc độ chéo không nhanh hơn), thêm check boundary tốt hơn (override clamp nếu cần), và tích hợp delta_time đầy đủ cho movement frame-independent.
  - Refine input: Sử dụng -=/+1 cho direction để hỗ trợ multi-key (chéo).
  - Thêm flip sprite theo hướng trái/phải (sử dụng original_image để tránh flip lặp).
  - Placeholder dodge: Khi SPACE, tăng speed tạm, set cooldown/duration với delta_time (cho mượt).
  - Thêm regen eggnergy theo thời gian (placeholder cho balance).
  - Tích Hợp Delta_Time Thực Trong game_screen.py Và main.py
- Ngày 18: Thêm dodge roll đầy đủ cho player với cooldown trong player.py. Chúng ta sẽ implement logic dodge: Khi nhấn SPACE (nếu cooldown hết), lăn né theo hướng hiện tại (tăng speed tạm thời, invincible trong duration ngắn), set cooldown để tránh spam, và reset sau.
- Ngày 19: Thêm melee attack (mổ tầm gần) cho player trong player.py. Đây là tấn công chính đầu tiên: Tốc độ nhanh, sát thương thấp, tạo hitbox phía trước player theo hướng (dựa direction), check collision với enemies (placeholder, vì enemy chưa có). Sử dụng input key (ví dụ: 'J' cho melee), với animation ngắn (placeholder tint hoặc delay), và damage từ constants.
- Ngày 20: Thêm ranged attack (bắn lông tầm xa) với eggnergy cho player trong player.py. Đây là tấn công thứ hai: Dùng năng lượng eggnergy (consume mỗi lần bắn), sát thương trung bình, tạo projectile bay theo hướng (placeholder vẽ line hoặc rect tạm, vì projectile.py sẽ ở Ngày 22).
- Ngày 21: Thêm bomb attack (đẻ trứng nổ) với limit cho player trong player.py. Đây là tấn công thứ ba: Sát thương cao, hạn chế số lượng (BOMB_LIMIT từ constants), tạo bomb tại vị trí player (hoặc ném theo hướng), explode sau delay hoặc collision, tạo AOE (area of effect) với BOMB_AOE_RADIUS. Sử dụng input key (ví dụ: 'L' cho bomb), check bomb_count > 0 mới đẻ, và regen limit theo thời gian hoặc collect (placeholder).
- Ngày 22: Tạo file projectile.py trong modules/entities/ để định nghĩa class Projectile kế thừa BaseEntity. Class này sẽ xử lý chung cho tất cả đạn: lông (ranged - bay thẳng), trứng (bomb - bay nhẹ rồi explode AOE). Điều này refactor placeholder dict trong player.py thành instances thực, dễ quản lý collision/damage/AI sau. Projectile có type ('ranged' hoặc 'bomb'), di chuyển theo direction, explode cho bomb, và remove khi out screen hoặc explode.
  - Kế thừa BaseEntity: Reuse movement (direction, speed, clamp - nhưng override clamp để không clamp projectile).
  - Type-specific: Ranged bay mãi đến out screen; Bomb countdown explode, vẽ AOE.
  - Placeholder draw: Circle màu theo type.
  - Sau: Load image từ assets, collision với enemies.
- Ngày 23: Tích hợp projectile vào player attacks đầy đủ, thêm collision cơ bản giữa projectile và entities (test với placeholder entity, vì enemy chưa có). Chúng ta sẽ refine player.py để handle collision (projectile hit thì apply damage, remove proj), thêm invincible check (không damage nếu player invincible), và refine Projectile để support collision.
- Ngày 24: Tạo file enemy.py trong modules/entities/ để định nghĩa class Enemy base kế thừa từ BaseEntity. Đây là foundation cho kẻ thù (cáo đỏ), với AI simple ban đầu: Di chuyển ngẫu nhiên (random direction thay đổi theo thời gian), speed từ constants, và placeholder cho behaviors phức tạp hơn sau (zigzag, keep distance, v.v.). Enemy sẽ có HP, damage (khi collide player), và drop thóc khi chết (placeholder).
  - Kế thừa BaseEntity: Reuse position, HP, movement, draw (HP bar).
  - AI simple: Change direction random mỗi 1-2s dùng timer delta_time, direction dùng math cho góc ngẫu nhiên.
  - Collision: Check chạm player thì damage (nếu không invincible), placeholder.
  - Drop: Khi chết, random drop thóc dựa DROP_THO_RATE (print tạm).
  - Type: Placeholder cho override (e.g., 'runner' zig-zag sau).
- Ngày 25: Thêm AI cho loại cáo chạy nhanh (type 'runner' - zig-zag áp sát) trong enemy.py. Chúng ta sẽ override update() để nếu có player target, enemy di chuyển zig-zag (lắc lư sin wave) hướng tới player, tốc độ nhanh (từ constants), và giữ distance ngắn để attack (cào vuốt placeholder).
- Ngày 26: Thêm AI cho cáo cung thủ (type 'archer' - giữ khoảng cách, bắn tên) trong enemy.py. Chúng ta sẽ refine update() để enemy giữ khoảng cách an toàn (ví dụ: 200-300 pixels từ player), né khi player quá gần (di chuyển ngược direction), và bắn tên (spawn Projectile ranged hướng tới player với cooldown ngắn). Điều này dựa trên gameplay (cáo cung thủ: giữ khoảng cách, né khi gà đến gần, bắn tên - dùng Projectile class để arrow như lông của player).

- Xem `docs/gameplay_design.md` để biết chi tiết gameplay.

## Kế hoạch dự án (dự kiến)
- Kế hoạch bao gồm:
  - Giai đoạn 1: Lập kế hoạch và Thiết lập (Ngày 1-20): Xây dựng nền tảng dự án.
  - Giai đoạn 2: Phát triển Core Gameplay (Ngày 21-80): Implement nhân vật, tấn công, di chuyển.
  - Giai đoạn 3: Phát triển Kẻ Thù và Boss (Ngày 81-120): Thêm AI và đối thủ.
  - Giai đoạn 4: Phát triển Hệ Thống Phụ (Ngày 121-160): Items, skills, map, safe zone.
  - Giai đoạn 5: Đồ Họa, Âm Thanh và Polish (Ngày 161-180): Tối ưu hóa trải nghiệm.
  - Giai đoạn 6: Testing và Hoàn Thiện (Ngày 181-200): Kiểm tra và hoàn tất.
- Cụ thể: 
  - Ngày 1: Nghiên cứu và cài đặt môi trường: Cài Python 3.8, Pygame, và các thư viện cần thiết (như pygame.mixer cho âm thanh). Tạo repository Git.
  - Ngày 2: Phân tích gameplay: Viết tài liệu chi tiết về các tính năng chính (nhân vật, kẻ thù, boss) dựa trên mô tả của bạn. 
  - Ngày 3: Thiết kế UML diagram cho các class chính (Player, Enemy, Item) bằng công cụ như Draw.io.
  - Ngày 4: Tạo thư mục dự án cơ bản (main.py, assets/, modules/).
  - Ngày 5: Viết constants.py trong utils/ để định nghĩa hằng số (màu sắc, kích thước màn hình, HP mặc định).
  - Ngày 6: Thiết lập main.py: Khởi tạo window Pygame cơ bản và loop chính.
  - Ngày 7: Thêm FPS counter và basic event handling trong main.py.
  - Ngày 8: Tạo module screens/: Viết game_screen.py với hàm draw background đơn giản.
  - Ngày 9: Tích hợp asset loading: Tạo assets/images/ và load một sprite test (gà con).
  - Ngày 10: Test run dự án cơ bản: Chạy main.py để hiển thị window với background.
  - Ngày 11: Viết helpers.py trong utils/ cho các hàm tiện ích (collision detection).
  - Ngày 12: Thiết kế database đơn giản (JSON) cho items và skills trong data/.
  - Ngày 13: Tạo module entities/: Viết base_entity.py cho class Entity chung.
  - Ngày 14: Kiểm tra và debug lỗi cơ bản trong setup.
  - Ngày 15: Viết tài liệu README.md cho dự án.
  - Ngày 16: Thiết kế level structure: Viết level_manager.py trong managers/.
  - Ngày 17: Thêm sound manager cơ bản trong managers/sound_manager.py.
  - Ngày 18: Tạo assets/sounds/ và load sound test.
  - Ngày 19: Commit Git và review giai đoạn 1.
  - Ngày 20: Buffer: Sửa lỗi hoặc nghiên cứu Pygame thêm nếu cần.
  - Ngày 21: Implement class Player trong entities/player.py: Thêm vị trí, di chuyển cơ bản (WASD).
  - Ngày 22: Thêm thanh HP cho Player và hiển thị HUD trong hud.py.
  - Ngày 23: Implement dodge roll cho Player: Thêm cooldown và animation cơ bản.
  - Ngày 24: Thêm tấn công gần (mổ): Logic sát thương và hitbox.
  - Ngày 25: Thêm tấn công xa (bắn lông): Sử dụng Eggnergy, projectile class trong entities/projectile.py.
  - Ngày 26: Thêm tấn công trứng nổ: Limit số lượng, explosion effect.
  - Ngày 27: Test player movement và attacks trong game_screen.py.
  - Ngày 28: Thêm energy bar (Eggnergy) cho Player.
  - Ngày 29: Implement skill system cơ bản trong skills.py: Class Skill base.
  - Ngày 30: Kết nối Player với skills: Mở khóa skill đầu tiên.
  - Ngày 31: Thêm thu thập thóc: Class Resource trong entities/resource.py.
  - Ngày 32: Logic mất thóc khi chết: Save/load thóc ở safe zone.
  - Ngày 33: Thiết kế safe zone (Chuồng Gà) trong screens/safe_zone.py.
  - Ngày 34: Implement hồi máu ở safe zone.
  - Ngày 35: Thêm shop trong safe_zone.py: Menu mua items.
  - Ngày 36: Implement skill tree: Random 3 skills mỗi lần nâng cấp.
  - Ngày 37: Thêm mission board: Nhiệm vụ đơn giản (kill X enemies).
  - Ngày 38: Nâng cấp chuồng: Logic giảm giá shop.
  - Ngày 39: Test safe zone integration.
  - Ngày 40: Buffer: Debug player và safe zone.
  - Ngày 41-50: Phát triển 3 nhánh skill tree (Chiến binh, Xạ thủ, Bom thủ): Mỗi ngày một nhánh, thêm 3-5 skills.
  - Ngày 51: Kết nối skill tree với Player.
  - Ngày 52: Thêm hiệu ứng hiệp lực items (synergy).
  - Ngày 53: Implement item system trong items.py: Class Item với rarity.
  - Ngày 54: Thêm ví dụ items (Mỏ thép, Bộ lông thép).
  - Ngày 55: Equip items cho Player.
  - Ngày 56: Test item effects trên attacks.
  - Ngày 57: Thêm map cơ bản: Wave-based arena trong level_manager.py.
  - Ngày 58: Spawn points cho enemies.
  - Ngày 59: Logic qua màn: Phá spawn points.
  - Ngày 60: Test core gameplay loop.
  - Ngày 61-70: Buffer và refine player mechanics (tăng tốc độ, sát thương theo items).
  - Ngày 71-80: Tối ưu hóa performance: Thêm quadtree cho collision nếu cần.
  - Ngày 81: Implement base Enemy trong entities/enemy.py.
  - Ngày 82: Thêm Cáo chạy nhanh: AI áp sát zig-zag.
  - Ngày 83: Thêm Cáo cung thủ: Giữ khoảng cách, né.
  - Ngày 84: Thêm Cáo ném bom: Tấn công diện rộng.
  - Ngày 85: Thêm Cáo giáp: Điểm yếu phía sau.
  - Ngày 86: Thêm Cáo pháp sư: Buff và vòng cản.
  - Ngày 87: Test enemy AI cơ bản.
  - Ngày 88: Thêm drop thóc từ enemies.
  - Ngày 89: Implement Boss base trong entities/boss.py.
  - Ngày 90: Boss 1 (Cáo Đại Tướng): Thương dài, lao.
  - Ngày 91: Thêm pha biến đổi cho Boss (3 pha).
  - Ngày 92: Spawn đàn cáo con ở 50% HP.
  - Ngày 93: Test boss fight.
  - Ngày 94: Tăng độ khó: Tốc độ enemies tăng theo wave.
  - Ngày 95: Boss học né: Adaptive AI đơn giản.
  - Ngày 96: Thêm đa dạng enemies theo wave.
  - Ngày 97: Integrate enemies vào level_manager.py.
  - Ngày 98: Test wave system.
  - Ngày 99: Buffer: Debug AI errors.
  - Ngày 100-110: Phát triển thêm boss cho màn sau (tương tự Boss 1, mỗi ngày một boss).
  - Ngày 111-120: Tích hợp boss mỗi 5 màn, test full level.
  - Ngày 121: Thêm môi trường map: Trang trại, rừng (background layers).
  - Ngày 122: Interactable objects (hũ, bụi rậm drop thóc).
  - Ngày 123: Logic rủi ro-thưởng: Mất thóc khi chết.
  - Ngày 124: Main menu trong screens/main_menu.py.
  - Ngày 125: Game over screen.
  - Ngày 126: Save/load game state (JSON).
  - Ngày 127: Implement Game+ mode: Khó hơn, skin mới.
  - Ngày 128: Thêm Đại Trùm Cáo Chúa ở màn cuối.
  - Ngày 129: Test endgame.
  - Ngày 130: Buffer: Refine systems.
  - Ngày 131-140: Thêm items và skills còn lại (mỗi ngày 2-3 items).
  - Ngày 141-150: Tích hợp synergy effects.
  - Ngày 151-160: Tối ưu hóa roguelite elements (random skills).
  - Ngày 161: Chuyển sang pixel art: Load sprites cho player, enemies.
  - Ngày 162: Animation cho attacks và dodge.
  - Ngày 163: Hiệu ứng lông văng thay máu.
  - Ngày 164: Background music theo wave.
  - Ngày 165: SFX: "Cục cục!", "Auu!".
  - Ngày 166: Test audio integration.
  - Ngày 167-170: Polish UI (HUD, menus).
  - Ngày 171-175: Thêm oblique projection view.
  - Ngày 176-180: Optimize graphics performance.
  - Ngày 181-190: Unit tests cho modules (player, enemy, etc.).
  - Ngày 191-195: Playtesting: Chơi qua full game, fix bugs.
  - Ngày 196: Build executable (pyinstaller).
  - Ngày 197: Documentation cuối cùng.
  - Ngày 198: Commit final Git.
  - Ngày 199: Buffer cho bất kỳ sửa chữa cuối.
  - Ngày 200: Hoàn thành: Release version 1.0.

# Promt để tiếp tục dự án khi bắt đầu một chat mới
Trả lời bằng tiếng việt. Tôi đã lên ý tưởng gameplay để lập trình game này hãy giúp tôi tạo dự án game này với python 3.8 và pygame, tạo thành nhiều module nhỏ để dễ quản lý và chỉnh sửa, Gameplay như sau: "THE CHICKENING – GAMEPLAY DESIGN
#### 1. Nhân vật chính: Gà con
* Có thanh HP, tốc độ di chuyển, sát thương (tùy theo trang bị).
* Có thể lăn né (dodge roll) để tránh đòn, cooldown ngắn.
* Sở hữu kỹ năng chủ động và bị động mở khóa dần theo màn.
* Có ba loại tấn công chính:
  1. Mổ tầm gần – tốc độ nhanh, sát thương thấp.
  2. Bắn lông tầm xa – dùng năng lượng (Eggnergy), sát thương trung bình.
  3. Đẻ trứng nổ – sát thương cao, hạn chế số lượng.
#### 2. Kẻ thù – Đội quân Cáo đỏ
Mỗi loại có hành vi (AI) riêng:
Loại cáoVũ khí/Kỹ năngHành viCáo chạy nhanhVuốt càoLiên tục áp sát, di chuyển zig-zagCáo cung thủBắn tênGiữ khoảng cách, né khi gà đến gầnCáo ném bomBom khoai tâyTấn công diện rộng, tạo vùng nguy hiểmCáo giápKhiên gỗChỉ lộ điểm yếu phía sauCáo pháp sư (màn sau)Lửa + triệu hồiBuff đồng đội, tạo vòng cản đường
#### 3. Trùm Cáo Đỏ (Boss)
* Mỗi 5 màn gặp 1 Boss cực mạnh
* Có 3 pha biến đổi (tăng tốc, dùng skill mới)
* Ví dụ Boss 1:
  * Cáo Đại Tướng: Dùng cây thương dài + lao về phía gà
  * Tạo đàn cáo con sau khi mất 50% HP
#### 4. Thu thập tài nguyên: Thóc
* Rơi từ quái hoặc xuất hiện trong hũ, bụi rậm
* Là tiền tệ để:
  * Mua trang bị
  * Mở kỹ năng
  * Nâng cấp chuồng để nhận buff toàn trận
Thu thập xong phải quay về Chuồng để lưu thóc → Nếu chết giữa chừng sẽ mất một phần thóc chưa cất.
Cơ chế rủi ro – thưởng (risk & reward)
#### 5. Chuồng Gà – Safe Zone
* Cáo đỏ không thể vào
* Nơi hồi máu & nâng cấp
* Các hạng mục:
  * Shop: vũ khí, áo giáp, phụ kiện (như Feather Cape tăng tốc, Egg Launcher tăng damage)
  * Skill Tree: chọn 1 trong 3 kỹ năng random theo phong cách roguelite
  * Mission Board: nhiệm vụ thưởng thêm thóc
Nâng cấp chuồng giúp giảm giá shop, mở skill mới, tăng regen HP.
#### 6. Bản đồ & Màn chơi
* Kiểu wave-based arena trong môi trường mở theo từng khu:
  * Trang trại, rừng thông, làng cáo, núi lửa,...
* Mỗi màn:
  * Gồm 5–10 đợt tấn công
  * Kẻ thù xuất hiện từ các hướng, có spawn point phá được
Phá được hết điểm spawn + tiêu diệt quái sẽ qua màn.
#### 7. Vật phẩm & Trang bị
Phân loại độ hiếm (Common → Legendary)
Ví dụ món đồ:
 Trang bịHiệu ứngMỏ thépTăng sát thương gầnBộ lông thépTăng giáp, giảm tốc độThần Lông Bất TửNé 1 đòn mỗi 15sGiày Phụt LôngTăng tốc + tạo sát thương khi lăn né
Các vật phẩm có hiệu ứng hiệp lực:
* “Lông cháy” + “Trứng xăng” → đánh gây cháy lâu hơn
#### 8. Kỹ năng (Skill Tree)
Ba nhánh phát triển:
1. Chiến binh Mỏ Sắt – sát thương cận chiến, tăng máu
2. Xạ thủ Xạ Lông – bắn xa, crit rate cao
3. Bom thủ Trứng Gà – trứng nổ mạnh, sát thương lan
Mỗi lần nâng cấp chọn 1 trong 3 kỹ năng ngẫu nhiên → tính chất roguelite, tăng replayability.
#### 9. AI và độ khó
* Theo thời gian, tốc độ và số lượng cáo tăng tiến tuyến tính
* Các đợt sau có đa dạng quái buộc người chơi phải thay đổi chiến thuật
* Boss học mô thức né nếu người chơi lạm dụng một kiểu đánh
#### 10. Đồ họa & Hiệu ứng
* Pixel art angled top-down / oblique projection
* Màu sắc tươi, dễ thương nhưng chiến đấu cảm giác “đã tay”
* Hiệu ứng máu chuyển sang lông văng để phù hợp rating + hài hước
#### 11. Âm thanh
* Nhạc vui, tiết tấu nhanh theo từng wave
* Hiệu ứng âm thanh dễ thương:
  * “Cục cục!” khi dùng kỹ năng
  * Cáo trúng đòn kêu “Auu!”
#### 12. Mục tiêu trò chơi
* Sống sót và qua từng màn
* Đánh bại Đại Trùm Cáo Chúa ở màn cuối
* Mở Game+ với quái khó hơn và skin mới"

### Cấu Trúc Dự Án

* the_chickening/

* ├── main.py # File chính chạy game, khởi tạo Pygame và loop

* ├── requirements.txt # Danh sách dependencies (pygame==2.1.2, etc.)

* ├── README.md # Tài liệu dự án

* ├── assets/ # Tài nguyên tĩnh

* │ ├── images/ # Sprites, backgrounds (e.g., chicken.png, fox.png)

* │ │ ├── player/

* │ │ │ ├── player/chicken.png

* │ │ ├── enemies/

* │ │ ├── items/

* │ │ └── backgrounds/

* │ └── sounds/ # Âm thanh (e.g., cluck.wav, auu.wav)

* ├── data/ # Dữ liệu JSON

* │ ├── items.json # Danh sách items và effects

* │ ├── skills.json # Skill tree data

* │ └── levels.json # Cấu trúc màn chơi

* ├── modules/ # Các module chính

* │ ├── entities/ # Các thực thể trong game

* │ │ ├── base_entity.py # Class Entity base (position, health, etc.)

* │ │ ├── player.py # Class Player (attacks, dodge, skills)

* │ │ ├── enemy.py # Class Enemy base (AI behaviors)

* │ │ ├── boss.py # Class Boss (phases, special attacks)

* │ │ ├── projectile.py # Đạn (lông, trứng nổ)

* │ │ └── resource.py # Thóc và drops

* │ ├── managers/ # Quản lý hệ thống

* │ │ ├── level_manager.py # Quản lý waves, spawns, maps

* │ │ ├── sound_manager.py # Quản lý nhạc và SFX

* │ │ └── item_manager.py # Quản lý items và synergies

* │ ├── screens/ # Các màn hình/game states

* │ │ ├── main_menu.py # Menu chính

* │ │ ├── game_screen.py # Màn chơi chính (arena)

* │ │ ├── safe_zone.py # Chuồng Gà (shop, skills, missions)

* │ │ └── game_over.py # Màn thua

* │ ├── utils/ # Công cụ hỗ trợ

* │ │ ├── constants.py # Hằng số (colors, sizes, etc.)

* │ │ ├── helpers.py # Hàm tiện ích (collision, random)

* │ │ └── hud.py # Heads-Up Display (HP, energy bar)

* │ └── skills.py # Hệ thống skills và tree (roguelite)

* └── tests/ # Unit tests (e.g., test_player.py

 
  Đầu tiên bạn hãy lên kế hoạch dự án theo ngày (tôi có quỹ thời gian là 200 ngày để hoàn thành), mỗi ngày đặt một mục tiêu cụ thể. Hãy tổ chức thư mục các module và các file của toàn bộ dự án
Sau đó, chúng ta đã thực hiện đến Ngày 11 theo hướng dẫn từng bước. Dự án đang ở giai đoạn setup cơ bản: có main.py với game loop, constants.py, game_screen.py với draw background và load sprite test (chicken.png), FPS counter, event handling cơ bản, helpers.py với collision detection và utility functions. Repo GitHub: https://github.com/Zakihung/The-Chickening.git
Bây giờ, hãy tiếp tục từ Ngày 12: Thiết kế database đơn giản (JSON) cho items và skills trong data/. Hãy cung cấp hướng dẫn chi tiết từng bước cho ngày này, tương tự các ngày trước.
Tôi thích phong cách tạo hướng dẫn theo kiểu này: "Hướng Dẫn Thực Hiện Ngày 5: Viết constants.py Trong utils/ Để Định Nghĩa Hằng Số
Chào bạn! Chúng ta đã hoàn thành Ngày 4 với cấu trúc thư mục cơ bản và main.py. Bây giờ là Ngày 5: Viết file constants.py trong thư mục modules/utils/ để định nghĩa các hằng số (constants) như màu sắc, kích thước màn hình, HP mặc định, v.v. Các hằng số này sẽ được sử dụng xuyên suốt dự án để tránh hardcode giá trị lặp lại, dễ chỉnh sửa sau (ví dụ: thay đổi kích thước màn hình chỉ cần sửa một chỗ).
Dựa trên tài liệu gameplay từ Ngày 2, chúng ta sẽ định nghĩa các giá trị cơ bản như SCREEN_WIDTH, COLORS, PLAYER_HP_DEFAULT, v.v. File này sẽ là module Python đơn giản, export các biến uppercase (convention cho constants).
Bước 1: Tạo File constants.py Trong PyCharm

1. Mở project The-Chickening.

2. Di chuyển đến thư mục modules/utils/ (nếu chưa có utils/, tạo nó: Right-click modules > New > Directory > utils).

3. Tạo file: Right-click utils > New > Python File > Đặt tên constants.py.

Bước 2: Viết Nội Dung Cho constants.py
Copy-paste code dưới đây vào file. Tôi đã chọn các hằng số thiết yếu dựa trên gameplay (có thể mở rộng sau):
Python

```
# modules/utils/constants.py
# Các hằng số chung cho game "The Chickening"

# Kích thước màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Màu sắc (RGB tuples)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)  # Cho thóc hoặc items

# Thuộc tính player mặc định
PLAYER_HP_DEFAULT = 100
PLAYER_SPEED_DEFAULT = 5  # pixels per frame
PLAYER_DAMAGE_DEFAULT = 10
EGGNERGY_MAX = 50
DODGE_COOLDOWN = 1000  # milliseconds (1 giây)

# Tấn công player
MELEE_RANGE = 50  # pixels
RANGED_RANGE = 300
BOMB_DAMAGE = 50
BOMB_AOE_RADIUS = 100
BOMB_LIMIT = 3

# Enemies
ENEMY_HP_BASE = 50
ENEMY_SPEED_BASE = 4
DROP_THO_RATE = 0.5  # Xác suất drop thóc (50%)

# Game settings
THOC_LOSS_ON_DEATH = 0.5  # Mất 50% thóc khi chết
WAVE_COUNT_PER_LEVEL = 5  # Số wave tối thiểu mỗi màn

# Paths (cho assets, sẽ dùng sau)
ASSETS_PATH = "../assets/"
IMAGES_PATH = ASSETS_PATH + "images/"
SOUNDS_PATH = ASSETS_PATH + "sounds/"
```

* Giải thích:

  * Các giá trị lấy từ gameplay_design.md (ví dụ: HP=100, tốc độ=5).

  * Sử dụng tuples cho màu sắc vì Pygame dùng RGB.

  * Có thể thêm comment để dễ hiểu.

  * Paths tương đối để load assets sau.

Bước 3: Test Import constants.py Trong main.py

1. Mở main.py, thêm import ở đầu:
   Python

   ```
   from modules.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BLACK
   ```

2. Sửa code trong main() để dùng constants:
   Python

   ```
   screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
   # ... (các phần khác giữ nguyên)
   screen.fill(COLOR_BLACK)
   clock.tick(FPS)
   ```

3. Chạy main.py (Right-click > Run). Nếu không lỗi và window hiện đúng kích thước, tốt!

Bước 4: Cập Nhật README.md (Tùy Chọn)
Thêm dòng vào phần Cấu Trúc Dự Án trong README.md:
Markdown

```
- `modules/utils/constants.py`: Định nghĩa hằng số toàn cục.
```

Bước 5: Commit Và Push Git

1. Add file: Right-click constants.py và update main.py > Git > Add.

2. Commit: VCS > Commit > Message: "Add constants.py with default values for screen, colors, player stats".

3. Push: VCS > Git > Push lên GitHub.

Bước 6: Hoàn Tất Ngày 5

* Thời gian ước tính: 30-45 phút.

* Kiểm tra: Import và dùng constants trong main.py không lỗi.

Ngày 5 hoàn thành! Bây giờ code đã sạch hơn với constants. Ngày mai (Ngày 6: Thiết lập main.py: Khởi tạo window Pygame cơ bản và loop chính), chúng ta sẽ refine main.py thêm. Nếu muốn chỉnh giá trị constants hoặc test thêm, cứ bảo nhé!"