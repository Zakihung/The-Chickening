# modules/managers/item_manager.py
import json
import random
from modules.utils.constants import DATA_PATH  # Add DATA_PATH = '../data/' in constants if need

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

    def get_random_item(self, rarity_chance={'Common': 0.5, 'Rare': 0.3, 'Epic': 0.15, 'Legendary': 0.05}):
        """Get random item id based rarity chance (on drop)."""
        rarity = random.choices(list(rarity_chance.keys()), weights=list(rarity_chance.values()))[0]
        rarity_items = [item['id'] for item in self.items_data if item['rarity'] == rarity]
        return random.choice(rarity_items) if rarity_items else None

    def equip_item(self, player, item_id):
        """Equip item to player slot, apply effects."""
        item = self.get_item_by_id(item_id)
        if item:
            type = item['type']  # weapon/armor/accessory
            if type in player.equipped_slots and player.equipped_slots[type]:
                self.unequip_item(player, player.equipped_slots[type])  # Swap unequip old
            player.equipped_slots[type] = item_id
            player.equipped_items.append(item_id)
            self.apply_effects(player, item['effects'], add=True)
            self.check_synergies(player)

    def remove_synergies(self, player):
        """Reset all synergy effects."""
        player.burn_damage = 0
        # Add more reset for other synergies (e.g., player.extra_speed = 0)

    def unequip_item(self, player, item_id):
        item = self.get_item_by_id(item_id)
        if item:
            player.equipped_items.remove(item_id)
            type = item['type']
            player.equipped_slots[type] = None
            self.apply_effects(player, item['effects'], add=False)
            self.remove_synergies(player)  # Reset synergies
            self.check_synergies(player)  # Reapply remaining

    def apply_effects(self, player, effects, add=True):
        """Apply/remove effects to player attrs."""
        mult = 1 if add else -1
        if 'melee_damage_bonus' in effects:
            player.melee_damage += mult * effects['melee_damage_bonus']
        if 'armor_bonus' in effects:
            player.armor += mult * effects['armor_bonus']
        if 'speed_penalty' in effects:
            player.speed += mult * effects['speed_penalty']  # Negative for penalty
        # Add more effects: dodge_chance, etc.

    def check_synergies(self, player):
        """Check combo, apply extra."""
        self.remove_synergies(player)  # Reset first
        equipped = player.equipped_items
        applied = set()  # Avoid duplicate apply
        for item_id in equipped:
            item = self.get_item_by_id(item_id)
            for syn in item['synergies']:
                if syn['with_item_id'] in equipped and (item_id, syn['with_item_id']) not in applied:
                    applied.add((item_id, syn['with_item_id']))
                    applied.add((syn['with_item_id'], item_id))  # Symmetric
                    if syn['effect'] == 'Tăng cháy lâu hơn':
                        player.burn_damage += 5
                    elif syn['effect'] == 'Cháy mạnh hơn với xăng':
                        player.bomb_damage += 10  # Placeholder
                    # Add more synergies from json (e.g., 'Tăng tốc + tạo sát thương khi lăn né' = dodge_damage +10)