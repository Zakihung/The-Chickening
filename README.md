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
- ├── highscores.json          `# Lưu highscores`
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
- │   │   ├── enemy.py         `# Class Enemy base (AI random, zig-zag cho 'runner', giữ khoảng cách/bắn tên cho 'archer', ném bom diện rộng cho 'bomber', giáp shield weak back cho 'shield', pháp sư buff/barrier cho 'mage')`
- │   │   ├── boss.py          `# Class Boss (phases đầy đủ cho Boss1: spear charge, frequent double, rage summon)`
- │   │   ├── projectile.py    `# Class Projectile (movement, explode, collision/damage handling)`
- │   │   └── resource.py      `# Class Resource (thóc drops, collect, thoc_collected/stored, die lose 50% with drop)`
- │   ├── managers/            `# Quản lý hệ thống`
- │   │   ├── level_manager.py `# Quản lý waves, spawns, levels từ json, level progression, boss every 5 levels integration, maps with bg and obstacles per type`
- │   │   ├── sound_manager.py `# Quản lý load/play SFX/music`
- │   │   └── item_manager.py  `# Quản lý items và synergies`
- │   ├── screens/             `# Các màn hình/game states`
- │   │   ├── main_menu.py     `# Menu chính với nút start/options/quit`
- │   │   ├── game_screen.py   `# Màn chơi chính (arena)`
- │   │   ├── safe_zone.py     `# Chuồng Gà (shop, skills, missions)`
- │   │   ├── game_over.py     `# Màn thua`
- │   │   └── options.py       `# Tùy chọn âm thanh, sfx`
- │   ├── utils/               `# Công cụ hỗ trợ`
- │   │   ├── constants.py     `# Hằng số (colors, sizes, etc.)`
- │   │   ├── helpers.py       `# Hàm tiện ích (collision, random)`
- │   │   └── hud.py           `# Heads-Up Display (HP, energy bar)`
- │   └── skills.py            `# Load/apply skills from json, random select roguelite, skill tree branches melee/ranged/bomb with apply, random roguelite selection per upgrade, integrate skills effects into player combat`
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
- Ngày 27: Thêm AI cho cáo ném bom (type 'bomber' - tấn công diện rộng) trong enemy.py. Chúng ta sẽ refine update() để enemy di chuyển ngẫu nhiên hoặc áp sát nhẹ, ném bom (spawn Projectile 'bomb' hướng tới player hoặc random) với cooldown, tạo vùng nguy hiểm AOE khi explode (dựa Projectile).
- Ngày 28: Thêm AI cho cáo giáp (type 'shield' - khiên gỗ, chỉ lộ điểm yếu phía sau) trong enemy.py. Chúng ta sẽ refine update() để enemy quay mặt về player (khiên phía trước - giảm damage 80% nếu hit front), thỉnh thoảng quay lưng (expose back - damage full x2), và attack melee khi quay lưng hoặc gần.
- Ngày 29: Thêm AI cho cáo pháp sư (type 'mage' - lửa + triệu hồi, buff đồng đội, tạo vòng cản đường) trong enemy.py. Chúng ta sẽ refine update() để enemy cast lửa (spawn Projectile 'ranged' lửa hướng player), buff nearby enemies (tăng speed/HP temp nếu có list), và tạo vòng cản (spawn 8 projectiles vòng tròn quanh self làm barrier - damage/slow player nếu chạm).
- Ngày 30: Tạo file boss.py trong modules/entities/ để định nghĩa class Boss kế thừa Enemy (hoặc BaseEntity), với phases cơ bản (3 pha: base, tăng tốc/skill mới khi <50% HP, summon minions khi <20%). Đây là foundation cho trùm (mỗi 5 level), ví dụ Boss 1 'Cáo Đại Tướng' (lao thương, summon cáo con). Boss sẽ có HP cao, size lớn, và transition phases (change AI/attacks).
  - Kế thừa Enemy: Reuse AI base, collision, drop.
  - Phases: Check hp_ratio change phase (tăng speed, summon).
  - AI Boss1: Charge direction player cooldown 3s (tăng speed temp).
  - Summon: Spawn Enemy 'runner' con yếu (HP/2), update/draw như projectiles.
  - Placeholder spear: Có thể spawn Projectile dài.
- Ngày 31: Thêm phase 1 chi tiết cho Boss 1 ('Cáo Đại Tướng') trong boss.py - lao với thương dài (dash nhanh về player với spear projectile dài hoặc extended melee, damage cao trong range dài). Phase 1 là base: Charge cooldown 3s, tăng speed dash 2x trong 1s, spawn spear (Projectile ranged dài, fast). Điều này dựa trên gameplay (Boss 1: Dùng cây thương dài + lao về phía gà).
- Ngày 32: Thêm phase 2-3 cho Boss trong boss.py (tăng tốc, dùng skill mới như summon minions sau 50% HP, và thêm attacks mới ở phase 3). Chúng ta sẽ refine update() để override phase-specific AI (phase 2: tăng speed + frequent charge, phase 3: summon + new skill như speed boost/rage mode).
- Ngày 33: Tạo file resource.py trong modules/entities/ để định nghĩa class Resource cho thóc drops (rơi từ enemies/boss khi chết, hoặc từ hũ/bụi rậm). Resource sẽ kế thừa BaseEntity (position, draw simple), collect khi player chạm (tăng thóc count, risk lose on death), và spawn random vị trí near enemy chết.
  - Kế thừa BaseEntity: Reuse position, update/draw.
  - Update: Collide player thì add amount to player.thoc (thêm player.thoc = 0 trong player.py), remove self.
  - Draw: Circle vàng (sau load sprite).
  - Spawn: Sẽ gọi từ enemy/boss khi die.
- Ngày 34: Tích hợp collect thóc với cơ chế rủi ro – thưởng (risk & reward). Player có thoc_collected (thóc nhặt giữa trận) và thoc_stored (thóc đã cất ở chuồng). Collect add to thoc_collected; khi die lose 50% thoc_collected (THOC_LOSS_ON_DEATH), drop remaining as Resource; quay về chuồng để store (thoc_stored += thoc_collected, reset collected).
- Ngày 35: Tạo file level_manager.py trong modules/managers/ để quản lý waves spawning (load từ levels.json, spawn enemies theo wave/level, check clear wave khi destroy all spawns/enemies). Manager sẽ hold list enemies, update/spawn theo time/wave, và progress level khi clear (boss every 5).
  - Load levels.json, select level data (waves, spawns as BaseEntity destructible).
  - Update: Spawn enemies từ random spawn_point per wave, timer delay.
  - Clear check: No enemies (sẽ add destroy all spawns sau).
  - Draw: Spawn/enemies.
- Ngày 36: Thêm spawn points phá hủy được trong level_manager.py (spawn_points là BaseEntity với HP, destroy khi hit projectile/melee, progress level khi all spawns destroyed + no enemies).
- Ngày 37: Quản lý level progression trong level_manager.py (5-10 waves/level từ WAVE_COUNT_PER_LEVEL, auto next level khi clear, boss every 5 levels spawn Boss thay waves, update progression (current_level tăng, load next json)).
- Ngày 38: Thêm boss every 5 levels đầy đủ trong level_manager.py (dựa current_level %5==0 spawn Boss thay waves, load boss data từ json nếu có, integrate summon minions, ensure clear when boss dead).
- Ngày 39: Tạo maps (farm, forest, village, volcano, etc.) trong level_manager.py (load background image từ assets dựa map_type/background json, draw background, add simple obstacles/environment entities từ map_type - placeholder rect block movement/collision).
- Ngày 40: Tạo file sound_manager.py trong modules/managers/ để load sounds (load SFX/music từ assets/sounds/, placeholder dict for sounds like cluck.wav, auu.wav, explosion.wav). Manager sẽ singleton-like, load on init, ready for play in Ngày 41.
- Ngày 41: Thêm play music và SFX đầy đủ trong sound_manager.py và entities (play music_wave.mp3 loop on wave start, SFX cluck on player skills, auu on enemy damage, explosion on bomb explode, refine volume/fade).
- Ngày 42: Tạo file item_manager.py trong modules/managers/ để quản lý load items từ data/items.json (list items with rarity/effects/synergies), equip to player (apply stats bonus), check synergies (combo effects if equipped multiple).
- Ngày 43: Thêm equip items cho player đầy đủ trong player.py và item_manager (add equipped_slots limit (weapon/armor/boots/accessory), unequip method reverse effects, test equip/unequip change stats/synergies).
- Ngày 44: Thêm synergies giữa items trong item_manager.py (check combo equipped items, apply extra effects like burn longer if “Lông cháy” + “Trứng xăng”, test multiple synergies activate/deactivate on equip/unequip).
- Ngày 45: Tạo file skills.py trong modules/ để load từ data/skills.json (ba branches melee/ranged/bomb với levels/effects, random 3 skills per upgrade roguelite style, apply selected to player).
  - Load skills.json to branches dict.
  - get_random_skills: Sample 3 from branch skills list (for choose 1 UI later).
  - apply_skill: Loop find skill by id, apply effects to player attrs (add player.crit_rate=0, unlocked_skills=[] in player.py).
  - Passive: Placeholder (refine in combat later, e.g., pierce bullet).
- Ngày 46: Thêm skill tree branches (melee, ranged, bomb) đầy đủ trong skills.py (branch melee: +damage/HP/close combat, ranged: +crit rate/pierce, bomb: +aoe radius/stun, apply branch on player choose upgrade, roguelite random per branch).
  - branches list from json keys.
  - apply_skill: Add branch-specific (melee +armor_mult, ranged pierce, bomb stun - add attrs in player).
  - choose_branch: Set player.branch (use for next upgrades random from branch).
  - Roguelite: Per upgrade, if player.branch, get_random from that, else choose branch first.
- Ngày 47: Thêm random selection roguelite trong skills.py (per upgrade get_random_skills 3 from player.branch, simulate choose 1 to apply, roguelite increase replayability by random each run).
- Ngày 48: Tích hợp skills vào player đầy đủ trong skills.py và player.py (apply skills effects to player combat (e.g., crit_rate on ranged hit damage *2 if random < rate, pierce hit multiple enemies, stun add timer to enemy no move), passive always on (e.g., armor_mult reduce damage in take_damage), test in game).
- Ngày 49: Tạo file main_menu.py trong modules/screens/ để định nghĩa class MainMenu (menu chính: buttons start game, options (placeholder), quit, use Pygame rect/text for clickable buttons, handle mouse click to transition states).
- Ngày 49.5: Tạo main_menu.py với buttons (menu state in main.py, click transition to game, options placeholder, quit), và test menu/buttons work in main.py. Bây giờ, tôi sẽ sửa nội dung các file đính kèm (enemy.py, player.py, main.py, game_screen.py, projectile.py, boss.py, skills.py, main_menu.py, item_manager.py, level_manager.py, sound_manager.py) để đảm bảo code nhất quán, remove test code (test equip/upgrade/skills in game_screen), integrate sound_manager triggers on events (attack/hit/explode/click), refine collision/drop/item/skill apply, fix potential errors (init lists before clear, pass sound_manager), and basic options screen placeholder. Không thực hiện bất kỳ thay đổi nào cho Ngày 50 hoặc sau.
- Ngày 49.9: Sửa toàn bộ các file liên quan
- Ngày 50: Tích hợp main_menu vào game loop đầy đủ trong main.py (state machine 'menu'/'game'/'options'/'game_over', on esc/die back to menu, options placeholder with back button, quit exit clean).
- Ngày 51-60: Tạo game_screen.py đầy đủ (tích hợp all entities/managers: player/enemies/boss/projectiles/resources/items/skills/sounds/level progression, update/draw all, handle states inside game like pause/safe_zone placeholder). 
  - Ngày 51: Integrate level_manager fully into game_screen (spawn/update/draw enemies/spawns/obstacles, player.enemies = level.enemies), remove test entities.
  - Ngày 52: Part 2 - integrate player/projectiles into game_screen (update/draw player/projectiles, collision check in screen or manager, refine projectile spawn from player attacks). Focus clean code, no duplicate update.
  - Ngày 53: Part 3 - integrate boss/minions into game_screen (boss as enemy in level_manager, minions update/draw from boss, ensure collision/damage with player/proj).
  - Ngày 54: Part 4 - integrate resources/thoc into game_screen (update/draw resources, collect add collected, die drop/loss, store_thoc on key/test).
  - Ngày 55: Part 5 - integrate items/equip into game_screen (item_manager in screen, random drop on enemy die add to inventory, equip on key/test, apply effects/synergies).
  - Ngày 55.9: Sửa lỗi các file
  - Ngày 56: Part 6 - integrate skills/upgrade into game_screen (skills in screen, upgrade on level clear (call upgrade_skill_tree if player.branch, apply selected), choose branch on key B test, apply to player combat full).
  - Ngày 57: Part 7 - integrate sounds on all events (pass sound_manager to entities/managers, trigger SFX on collect/drop/upgrade/level clear, music change on boss level).
  - Ngày 58: Part 8 - add hud in game_screen (HP/energy/thoc counter text/bar, minimap placeholder rect show enemies/obs).
  - Ngày 59: Part 9 - add pause/safe_zone in game_screen (key P pause (stop update, draw 'Paused'), key S to safe_zone state (store thóc, shop/skills placeholder, back on esc).
  - Ngày 60: Part 10 - refine full game_screen (all integrated: entities/managers/states/hud/sounds/items/skills, test complete flow level/wave/boss/clear/upgrade/equip/drop/collect/die, remove test damage, optimize no errors).
  - Ngày 60.9: Sửa lỗi các file
- Ngày 61-70: Tạo safe_zone.py Với Shop, Skills, Missions
  - Ngày 61: Part 1 - create safe_zone.py with basic shop (buy items from list with thoc_stored, apply equip), skills upgrade (call skills.upgrade_tree on button, choose from 3 random UI placeholder text), missions board (placeholder tasks reward thoc).
  - Ngày 62: Part 2 - refine shop in safe_zone (display items list from item_manager, buy button per item if affordable, deduct thoc_stored).
  - Ngày 63: Part 3 - add skills upgrade UI in safe_zone (button show 3 random from branch, sub-buttons choose 1 apply, cost thoc if need placeholder 100).
  - Ngày 64: Part 4 - add missions board in safe_zone (list 3 tasks e.g., 'Kill 5 enemies' reward 100 thoc, complete check on level clear or kill, button claim reward add thoc_stored).
  - Ngày 65: Part 5 - refine shop with rarity/price (price based rarity Common 50, Legendary 500, display color rarity), buy deduct thoc_stored.
  - Ngày 66: Part 6 - add upgrade chuồng in safe_zone (button upgrade reduce shop price/increase regen HP, cost thoc_stored increasing levels).
  - Ngày 67: Part 7 - refine skills UI in safe_zone (draw 3 random skills text/effects as buttons, on click apply selected, cost thoc per upgrade).
  - Ngày 68: Part 8 - refine missions (multiple tasks 'Kill X type' 'Destroy spawns', progress track in player.mission_progress dict, claim reward on complete).
  - Ngày 69: Part 9 - add draw thoc_stored text in safe_zone, refine shop discount from chuong_level (price = (1 - 0.1level)).
  - Ngày 70: Part 10 - refine full safe_zone (all integrated shop/buy/equip, skills choose 3 apply, missions claim, upgrade chuong apply buffs, test flow enter S, actions, back esc, optimize no errors).
- Ngày 71-80: Tạo game_over.py và state transitions.
  - Ngày 71: Part 1/10 - refine game_over.py with functional buttons (restart new game_screen, quit exit), draw score placeholder.
  - Ngày 72: Part 2/10 - refine main.py state transitions for die (check player.alive = False to 'game_over').
  - Ngày 73: Part 3/10 - refine main.py on game_over 'restart' action new GameScreen, back to 'game'.
  - Ngày 74: Part 4/10 - refine main.py on game_over 'quit' running = False clean exit.
  - Ngày 75: Part 5/10 - refine main.py esc in 'game' state = 'menu'.
  - Ngày 76: Part 6/10 - add options state in main.py, placeholder with vol slider for music/sfx (use mouse drag adjust sound_manager vol).
  - Ngày 77: Part 7/10 - add highscore in game_over.py (load/save json highscores, draw top 5, update on die with score = thoc_stored + levels cleared).
  - Ngày 78: Part 8/10 - add score calc in game_screen (score = thoc + levels100 + kills10, update on collect/clear/kill, pass to game_over on die).
  - Ngày 79: Part 9/10 - add fade in/out on state transitions in main.py (use pygame surface alpha fade for smooth change).
  - Ngày 80: Part 10/10 - refine full state transitions (all states menu/game/options/game_over/safe_zone/pause, test flow start/play/die/restart/options/back/quit/esc, optimize no errors, clean code).
- Ngày 81-90: Add Pixel Art Assets
  - Ngày 81: Part 1 - add pixel art for player (chicken.png in assets/images/player/, load/scale in player.py init, draw blit if image).
  - Ngày 82: Part 2 - add sprites for enemies types (fox_runner.png, archer.png etc. in assets/images/enemies/, load in enemy.py init based type).
  - Ngày 83: Part 3 - add sprites for projectiles (feather.png ranged, egg.png bomb, spear.png boss, load in projectile.py init based type).
  - Ngày 84: Part 4 - add sprite for thóc (thoc.png in assets/images/resources/, load in resource.py init).
  - Ngày 85: Part 5 - add icons for items (mo_thep.png etc. in assets/images/items/, load in item_manager but UI draw later in safe_zone shop).
  - Ngày 86: Part 6 - add bg images (farm_bg.png, forest_bg.png etc. in assets/images/backgrounds/, load in level_manager load_level).
  - Ngày 87: Part 7 - add sprites for obstacles (tree.png, bush.png in assets/images/obstacles/, load in level_manager load_level based map_type random).
  - Ngày 88: Part 8 - add sprite for spawns (spawn_point.png in assets/images/spawns/, load in level_manager spawn_points BaseEntity image).
  - Ngày 89: Part 9 - add sprite for boss (big_fox.png in assets/images/boss/, load in boss.py init scale 100x100).
  - Ngày 90: Part 10 - add sprite for minions (small_fox.png in assets/images/minions/, load in boss.summon_minions Enemy init scale 30x30), full test all assets load/draw no errors, optimize.

#### Xem `docs/gameplay_design.md` để biết chi tiết gameplay.

### Link grok to day 90.5
https://grok.com/share/c2hhcmQtMw_30572994-aa8b-41fa-8614-4417bfa96c97

### Link grok to day 90.9
https://grok.com/share/c2hhcmQtMw_ffa0f216-2129-478a-b9a5-b7f6bda39dfa

#### Ghi chú tạm
Sửa lại nội dung của các file đính kèm (game_over.py, main.py, options.py, highscores.json, game_screen.py, player.py) đến ngày 80, không thực hiện hướng dẫn ngày 81

## Kế hoạch dự án 1 (dự kiến)
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

## Kế hoạch dự án 2 (dự kiến)
  - Ngày 1-11: (Đã hoàn thành theo bạn: Setup repo, main.py, constants.py, game_screen.py với background/sprite test, FPS, events, helpers.py với collision).
  - Ngày 12: Thiết kế database đơn giản (JSON) cho items và skills trong data/ (chi tiết hướng dẫn ở phần sau).
  - Ngày 13: Thiết kế levels.json trong data/ cho cấu trúc màn chơi.
  - Ngày 14: Tạo base_entity.py trong entities/ với position, health cơ bản.
  - Ngày 15: Thêm update và draw methods vào base_entity.py.
  - Ngày 16: Tạo player.py kế thừa base_entity, thêm HP, speed.
  - Ngày 17: Thêm input handling cho player movement trong player.py.
  - Ngày 18: Thêm dodge roll cho player với cooldown.
  - Ngày 19: Thêm melee attack (mổ) cho player.
  - Ngày 20: Thêm ranged attack (bắn lông) với eggnergy.
  - Ngày 21: Thêm bomb attack (đẻ trứng nổ) với limit.
  - Ngày 22: Tạo projectile.py cho đạn (lông, trứng).
  - Ngày 23: Tích hợp projectile vào player attacks.
  - Ngày 24: Tạo enemy.py base với AI simple (di chuyển ngẫu nhiên).
  - Ngày 25: Thêm AI cho cáo chạy nhanh (zig-zag áp sát).
  - Ngày 26: Thêm AI cho cáo cung thủ (giữ khoảng cách, bắn tên).
  - Ngày 27: Thêm AI cho cáo ném bom (tấn công diện rộng).
  - Ngày 28: Thêm AI cho cáo giáp (điểm yếu phía sau).
  - Ngày 29: Thêm AI cho cáo pháp sư (buff, vòng cản).
  - Ngày 30: Tạo boss.py với phases cơ bản.
  - Ngày 31: Thêm phase 1 cho Boss 1 (lao với thương).
  - Ngày 32: Thêm phase 2-3 cho Boss (summon, tăng tốc).
  - Ngày 33: Tạo resource.py cho thóc drops.
  - Ngày 34: Tích hợp collect thóc với rủi ro (mất khi chết).
  - Ngày 35: Tạo level_manager.py với wave spawning.
  - Ngày 36: Thêm spawn points phá hủy được.
  - Ngày 37: Quản lý level progression (5-10 waves/level).
  - Ngày 38: Thêm boss every 5 levels.
  - Ngày 39: Tạo maps (farm, forest, etc.) trong level_manager.
  - Ngày 40: Tạo sound_manager.py để load sounds.
  - Ngày 41: Thêm play music và SFX.
  - Ngày 42: Tạo item_manager.py để load từ items.json.
  - Ngày 43: Thêm equip items cho player.
  - Ngày 44: Thêm synergies giữa items.
  - Ngày 45: Tạo skills.py để load từ skills.json.
  - Ngày 46: Thêm skill tree branches (melee, ranged, bomb).
  - Ngày 47: Thêm random selection roguelite.
  - Ngày 48: Tích hợp skills vào player.
  - Ngày 49: Tạo main_menu.py với buttons.
  - Ngày 50: Tích hợp main_menu vào game loop.
  - Ngày 51-60: Tạo game_screen.py đầy đủ (tích hợp entities, managers).
  - Ngày 61-70: Tạo safe_zone.py với shop, skills, missions.
  - Ngày 71-80: Tạo game_over.py và state transitions.
  - Ngày 81-90: Refine HUD trong hud.py (HP, energy, thóc).
  - Ngày 91-100: Thêm effects (pixel art animations, lông văng).
  - Ngày 101-110: Cải thiện AI độ khó (tăng dần, học pattern).
  - Ngày 111-120: Thêm synergies và rarities cho items/skills.
  - Ngày 121-130: Load assets (images, sounds) đầy đủ.
  - Ngày 131-140: Thêm environments (backgrounds, obstacles).
  - Ngày 141-150: Polish combat feel (hit feedback, sounds).
  - Ngày 151-160: Thêm missions board và coop upgrades.
  - Ngày 161-170: Optimize performance (FPS, collision).
  - Ngày 171-180: Viết unit tests cho các module chính.
  - Ngày 181-190: Debug toàn bộ, fix bugs từ gameplay.
  - Ngày 191-195: Thêm New Game+ mode với skins.
  - Ngày 196-198: Update README.md đầy đủ, add docs.
  - Ngày 199: Build executable (pyinstaller nếu cần).
  - Ngày 200: Release on GitHub, test final.

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