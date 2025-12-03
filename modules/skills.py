# modules/skills.py
import json
import random
from modules.utils.constants import DATA_PATH

class Skills:
    def __init__(self):
        """
        Hệ thống skills: Load từ skills.json, random select, apply to player.
        """
        with open(DATA_PATH + 'skills.json', 'r', encoding="utf8") as f:
            self.skills_data = json.load(f)['branches']  # Dict branches {melee: {skills: list}}

    def get_random_skills(self, branch, count=3):
        """Return random 3 skills from branch (roguelite choose 1)."""
        branch_skills = self.skills_data.get(branch, {}).get('skills', [])
        if len(branch_skills) < count:
            return branch_skills
        return random.sample(branch_skills, count)

    def apply_skill(self, player, skill_id):
        """Apply skill effects to player."""
        for branch in self.skills_data.values():
            skill = next((s for s in branch['skills'] if s['id'] == skill_id), None)
            if skill:
                effects = skill['effects']
                if 'melee_damage_bonus' in effects:
                    player.melee_damage += effects['melee_damage_bonus']
                if 'hp_bonus' in effects:
                    player.max_hp += effects['hp_bonus']
                    player.hp += effects['hp_bonus']
                if 'crit_rate' in effects:
                    player.crit_rate = effects['crit_rate']  # Add player.crit_rate = 0 in init
                if 'passive' in effects:
                    # Placeholder passive (e.g., player.pierce = True for 'Bắn xuyên')
                    player.unlocked_skills.append(skill_id)  # List unlocked
                return True
        return False