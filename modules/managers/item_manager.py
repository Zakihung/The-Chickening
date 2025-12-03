# modules/managers/item_manager.py
import json
import random
from modules.utils.constants import DATA_PATH

class ItemManager:
    def __init__(self):
        with open(DATA_PATH + 'items.json', 'r', encoding="utf8") as f:
            self.items_data = json.load(f)['items']
        self.synergies = {}

    def get_item_by_id(self, item_id):
        return next((item for item in self.items_data if item['id'] == item_id), None)

    def get_random_item(self, rarity_chance={'Common': 0.5, 'Rare': 0.3, 'Epic': 0.15, 'Legendary': 0.05}):
        rarity = random.choices(list(rarity_chance.keys()), weights=list(rarity_chance.values()))[0]
        rarity_items = [item['id'] for item in self.items_data if item['rarity'] == rarity]
        return random.choice(rarity_items) if rarity_items else None

    def equip_item(self, player, item_id):
        item = self.get_item_by_id(item_id)
        if item:
            type = item['type']
            if type in player.equipped_slots and player.equipped_slots[type]:
                self.unequip_item(player, player.equipped_slots[type])
            player.equipped_slots[type] = item_id
            player.equipped_items.append(item_id)
            self.apply_effects(player, item['effects'], add=True)
            self.check_synergies(player)

    def unequip_item(self, player, item_id):
        item = self.get_item_by_id(item_id)
        if item:
            player.equipped_items.remove(item_id)
            type = item['type']
            player.equipped_slots[type] = None
            self.apply_effects(player, item['effects'], add=False)
            self.remove_synergies(player)
            self.check_synergies(player)

    def apply_effects(self, player, effects, add=True):
        mult = 1 if add else -1
        if 'melee_damage_bonus' in effects:
            player.melee_damage += mult * effects['melee_damage_bonus']
        if 'armor_bonus' in effects:
            player.armor += mult * effects['armor_bonus']
        if 'speed_penalty' in effects:
            player.speed += mult * effects['speed_penalty']
        if 'dodge_chance' in effects:
            player.dodge_chance += mult * effects['dodge_chance']  # Add player.dodge_chance = 0

    def remove_synergies(self, player):
        player.burn_damage = 0

    def check_synergies(self, player):
        self.remove_synergies(player)
        equipped = player.equipped_items
        applied = set()
        for item_id in equipped:
            item = self.get_item_by_id(item_id)
            for syn in item['synergies']:
                if syn['with_item_id'] in equipped and (item_id, syn['with_item_id']) not in applied:
                    applied.add((item_id, syn['with_item_id']))
                    applied.add((syn['with_item_id'], item_id))
                    if syn['effect'] == 'Tăng cháy lâu hơn':
                        player.burn_damage += 5
                    elif syn['effect'] == 'Cháy mạnh hơn với xăng':
                        player.bomb_damage += 10