import pygame
from modules.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BLACK, COLOR_WHITE, COLOR_BLUE

class SafeZone:
    def __init__(self, screen, player, item_manager, skills):
        """
        Chuồng Gà - Safe Zone: Shop, skills, missions, upgrade chuồng.
        """
        self.screen = screen
        self.player = player
        self.item_manager = item_manager
        self.skills = skills
        self.buttons = [
            {'text': 'Store Thóc', 'rect': pygame.Rect(SCREEN_WIDTH//2 - 100, 100, 200, 50), 'action': 'store'},
            {'text': 'Shop', 'rect': pygame.Rect(SCREEN_WIDTH//2 - 100, 200, 200, 50), 'action': 'shop'},
            {'text': 'Skills Upgrade', 'rect': pygame.Rect(SCREEN_WIDTH//2 - 100, 300, 200, 50), 'action': 'skills'},
            {'text': 'Missions', 'rect': pygame.Rect(SCREEN_WIDTH//2 - 100, 400, 200, 50), 'action': 'missions'},
            {'text': 'Upgrade Chuồng', 'rect': pygame.Rect(SCREEN_WIDTH//2 - 100, 500, 200, 50), 'action': 'upgrade'},
            {'text': 'Back', 'rect': pygame.Rect(SCREEN_WIDTH//2 - 100, 600, 200, 50), 'action': 'back'}
        ]
        self.font = pygame.font.SysFont(None, 40)
        self.small_font = pygame.font.SysFont(None, 30)
        self.shop_items = self.item_manager.items_data[:5]  # Placeholder 5 items
        self.shop_buttons = []  # Dynamic buy buttons
        self.skills_options = []  # 3 random skills buttons
        self.missions = [
            {'task': 'Kill 5 runner', 'progress_key': 'kill_runner', 'goal': 5, 'reward': 100},
            {'task': 'Destroy 3 spawns', 'progress_key': 'destroy_spawn', 'goal': 3, 'reward': 150},
            {'task': 'Collect 50 thóc', 'progress_key': 'collect_thoc', 'goal': 50, 'reward': 200}
        ]
        self.mission_buttons = []  # Claim buttons
        self.shop_discount = 0.1 * self.player.chuong_level  # From upgrade
        self.show_shop = False
        self.show_skills = False
        self.show_missions = False

    def update(self, events):
        """Handle click return action."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button['rect'].collidepoint(mouse_pos):
                        if button['action'] == 'store':
                            self.player.store_thoc()
                        elif button['action'] == 'shop':
                            self.show_shop = not self.show_shop
                            self.shop_buttons = self.create_shop_buttons()
                        elif button['action'] == 'skills':
                            self.show_skills = not self.show_skills
                            self.skills_options = self.create_skills_buttons()
                        elif button['action'] == 'missions':
                            self.show_missions = not self.show_missions
                            self.mission_buttons = self.create_mission_buttons()
                        elif button['action'] == 'upgrade':
                            self.upgrade_chuong()
                        elif button['action'] == 'back':
                            return 'back'
                # Check sub-buttons
                if self.show_shop:
                    for btn in self.shop_buttons:
                        if btn['rect'].collidepoint(mouse_pos):
                            self.buy_item(btn['item_id'])
                if self.show_skills:
                    for btn in self.skills_options:
                        if btn['rect'].collidepoint(mouse_pos):
                            self.apply_skill(btn['skill_id'])
                            self.show_skills = False
                if self.show_missions:
                    for btn in self.mission_buttons:
                        if btn['rect'].collidepoint(mouse_pos):
                            self.claim_mission(btn['mission_index'])
        return None

    def draw(self):
        """Draw safe zone."""
        self.screen.fill(COLOR_BLUE)
        thoc_text = self.small_font.render(f"Thóc Stored: {self.player.thoc_stored}", True, COLOR_WHITE)
        self.screen.blit(thoc_text, (10, 10))
        for button in self.buttons:
            pygame.draw.rect(self.screen, COLOR_BLACK, button['rect'])
            text = self.font.render(button['text'], True, COLOR_WHITE)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)

        if self.show_shop:
            for btn in self.shop_buttons:
                pygame.draw.rect(self.screen, COLOR_BLACK, btn['rect'])
                text = self.small_font.render(f"{btn['name']} ({btn['price']})", True, COLOR_WHITE)
                text_rect = text.get_rect(center=btn['rect'].center)
                self.screen.blit(text, text_rect)

        if self.show_skills:
            for btn in self.skills_options:
                pygame.draw.rect(self.screen, COLOR_BLACK, btn['rect'])
                text = self.small_font.render(btn['name'], True, COLOR_WHITE)
                text_rect = text.get_rect(center=btn['rect'].center)
                self.screen.blit(text, text_rect)

        if self.show_missions:
            for i, mission in enumerate(self.missions):
                progress = self.player.mission_progress.get(mission['progress_key'], 0)
                text = self.small_font.render(f"{mission['task']} {progress}/{mission['goal']} Reward: {mission['reward']}", True, COLOR_WHITE)
                self.screen.blit(text, (SCREEN_WIDTH//2 - 200, 100 + i*50))
            for btn in self.mission_buttons:
                pygame.draw.rect(self.screen, COLOR_BLACK, btn['rect'])
                text = self.small_font.render('Claim', True, COLOR_WHITE)
                text_rect = text.get_rect(center=btn['rect'].center)
                self.screen.blit(text, text_rect)

    def create_shop_buttons(self):
        buttons = []
        for i, item in enumerate(self.shop_items):
            price = item.get('price', 100) * (1 - self.shop_discount)
            btn = {'item_id': item['id'], 'name': item['name'], 'price': price, 'rect': pygame.Rect(SCREEN_WIDTH//2 + 100, 100 + i*60, 200, 50)}
            buttons.append(btn)
        return buttons

    def buy_item(self, item_id):
        item = self.item_manager.get_item_by_id(item_id)
        price = item.get('price', 100) * (1 - self.shop_discount)
        if self.player.thoc_stored >= price:
            self.player.thoc_stored -= price
            self.player.inventory.append(item_id)
            print(f"Bought {item['name']}")

    def create_skills_buttons(self):
        random_skills = self.skills.get_random_skills(self.player.branch, 3)
        buttons = []
        for i, skill in enumerate(random_skills):
            btn = {'skill_id': skill['id'], 'name': skill['name'], 'rect': pygame.Rect(SCREEN_WIDTH//2 + 100, 100 + i*60, 200, 50)}
            buttons.append(btn)
        return buttons

    def apply_skill(self, skill_id):
        if self.player.thoc_stored >= 100:
            self.player.thoc_stored -= 100
            self.skills.apply_skill(self.player, skill_id)
            print(f"Applied skill {skill_id}")

    def create_mission_buttons(self):
        buttons = []
        for i, mission in enumerate(self.missions):
            progress = self.player.mission_progress.get(mission['progress_key'], 0)
            if progress >= mission['goal']:
                btn = {'mission_index': i, 'rect': pygame.Rect(SCREEN_WIDTH//2 + 300, 100 + i*50, 100, 40)}
                buttons.append(btn)
        return buttons

    def claim_mission(self, index):
        mission = self.missions[index]
        progress = self.player.mission_progress.get(mission['progress_key'], 0)
        if progress >= mission['goal']:
            self.player.thoc_stored += mission['reward']
            self.player.mission_progress[mission['progress_key']] = 0  # Reset
            print(f"Claimed {mission['reward']} thóc")

    def upgrade_chuong(self):
        if self.player.chuong_level < 3:
            cost = 200 * (self.player.chuong_level + 1)
            if self.player.thoc_stored >= cost:
                self.player.thoc_stored -= cost
                self.player.chuong_level += 1
                self.player.regen_hp += 10  # Buff
                self.shop_discount = 0.1 * self.player.chuong_level
                print(f"Upgraded chuồng to level {self.player.chuong_level}")