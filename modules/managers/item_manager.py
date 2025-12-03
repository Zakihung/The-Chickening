# modules/managers/item_manager.py
import json
from modules.utils.constants import DATA_PATH

class ItemManager:
    def __init__(self):
        """
        Quản lý items: Load từ items.json, equip/apply effects to player.
        """
        with open(DATA_PATH + 'items.json', 'r', encoding="utf8") as f:
            self.items_data = json.load(f)['items']  # List dict items
        self.synergies = {}  # Dict for quick synergy check (build from data)

    def get_item_by_id(self, item_id):
        """Get item dict by id."""
        return next((item for item in self.items_data if item['id'] == item_id), None)

    def equip_item(self, player, item_id):
        """Equip item to player, apply effects."""
        item = self.get_item_by_id(item_id)
        if item:
            # Apply effects (placeholder player attrs)
            effects = item['effects']
            if 'melee_damage_bonus' in effects:
                player.melee_damage += effects['melee_damage_bonus']
            if 'armor_bonus' in effects:
                player.armor += effects['armor_bonus']  # Add player.armor = 0 in init
            # Add more: speed_penalty, dodge_chance, etc.
            player.equipped_items.append(item_id)  # List equipped ids in player
            self.check_synergies(player)

    def check_synergies(self, player):
        """Check combo between equipped items, apply extra effects."""
        equipped = player.equipped_items
        for item_id in equipped:
            item = self.get_item_by_id(item_id)
            for syn in item['synergies']:
                if syn['with_item_id'] in equipped:
                    # Apply synergy effect (placeholder)
                    if syn['effect'] == 'Tăng cháy lâu hơn':
                        player.burn_damage += 5  # Extra burn
                    # Add more synergies

    def unequip_item(self, player, item_id):
        """Unequip, reverse effects (placeholder)."""
        pass