# modules/skills.py
import json
import random
from modules.utils.constants import DATA_PATH

class Skills:
    def __init__(self):
        with open(DATA_PATH + 'skills.json', 'r', encoding="utf8") as f:
            self.skills_data = json.load(f)['branches']

        self.branches = list(self.skills_data.keys())
        self.upgrade_levels = {'melee': 0, 'ranged': 0, 'bomb': 0}

    def get_random_skills(self, branch, count=3):
        branch_skills = self.skills_data.get(branch, {}).get('skills', [])
        if len(branch_skills) < count:
            return branch_skills
        return random.sample(branch_skills, count)

    def upgrade_skill_tree(self, player):
        if player.branch:
            random_skills = self.get_random_skills(player.branch, 3)
            if random_skills:
                selected = random_skills[0]  # Placeholder choose first
                if self.apply_skill(player, selected['id']):
                    self.upgrade_levels[player.branch] += 1
                    return selected
        return None

    def apply_skill(self, player, skill_id):
        for branch, data in self.skills_data.items():
            skill = next((s for s in data['skills'] if s['id'] == skill_id), None)
            if skill:
                effects = skill['effects']
                if 'melee_damage_bonus' in effects:
                    player.melee_damage += effects['melee_damage_bonus']
                if 'hp_bonus' in effects:
                    player.max_hp += effects['hp_bonus']
                    player.hp += effects['hp_bonus']
                if 'crit_rate' in effects:
                    player.crit_rate = effects['crit_rate']
                if 'bomb_damage_bonus' in effects:
                    player.bomb_damage += effects['bomb_damage_bonus']
                if 'aoe_radius_bonus' in effects:
                    player.bomb_aoe_radius += effects['aoe_radius_bonus']
                if 'passive' in skill:
                    if skill['passive'] == 'Tăng giáp 10%':
                        player.armor_mult *= 1.1
                    elif skill['passive'] == 'Bắn xuyên 1 kẻ thù':
                        player.ranged_pierce += 1
                    elif skill['passive'] == 'Trứng gây stun 2s':
                        player.bomb_stun += 2.0
                player.unlocked_skills.append(skill_id)
                player.branch = branch
                return True
        return False

    def choose_branch(self, player, branch):
        if branch in self.branches:
            player.branch = branch
            return True
        return False