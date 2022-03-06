import requests
import json
from modules.Data import Data

class Ahri():
    def __init__(self):
        self.name       = "ahri"
        self.name_upper = "Ahri"

        self.ap    = 0
        self.m_pen = 0
        self.tiers = {
            "q": 1,
            "w": 1,
            "e": 1,
            "r": 1,
        }

        ## Fetch data from API
        data     = Data()
        url      = f"{data.base_url}/{data.patch}/game/data/characters/{self.name}/{self.name}.bin.json"
        response = requests.get(url)
        self.response_data = json.loads(response.text)

    def get_ap(self):
        return self.ap

    def get_m_pen(self):
        return self.ap

    def get_tiers(self):
        return self.tiers

    def set_ap(self, ap):
        if ap >= 0: self.ap = ap
        else: print(f"Cannot set ap to {ap}")
        return None

    def set_m_pen(self, m_pen):
        if m_pen >= 0: self.m_pen = m_pen
        else: print(f"Cannot set m_pen to {m_pen}")
        return None

    def add_ap(self, ap):
        if self.ap + ap >= 0: self.ap += ap
        else: print(f"Cannot add {ap} ap")
        return None

    def add_m_pen(self, m_pen):
        if self.m_pen + m_pen >= 0: self.m_pen += m_pen
        else: print(f"Cannot add {m_pen} m_pen")
        return None

    def set_tiers(self, tiers):
        try:
            if tiers["q"] not in [1,2,3,4,5] or tiers["w"] not in [1,2,3,4,5] or tiers["e"] not in [1,2,3,4,5] or tiers["r"] not in [1,2,3]:     
                print(f"Invalid tiers: {tiers}")
                return None
            else: self.tiers = tiers
        except KeyError:
            print(f"Invalid tiers: {tiers}")
        return None

    def add_tier(self, spell, amount):
        try:
            if (spell in ["q","w","e"] and self.tiers[spell] + amount not in [1,2,3,4,5]) or (spell == "r" and self.tiers[spell] + amount not in [1,2,3]):
                print(f"Invalid spell: {spell}")
                return None
        except KeyError:
            print(f"Invalid spell: {spell}")
        return None


    def invalid_tier_or_ap(self, tier, ap, spell_name, missiles=None, isUlt=False):
        if tier not in [1,2,3,4,5] or (isUlt and tier not in [1,2,3]):
            print(f"Invalid tier '{tier}' for {spell_name} given")
            return True
        if ap < 0:
            print(f"Invalid ap '{ap}' for {spell_name} given")
            return True
        if missiles is not None:
            if missiles not in [1,2,3]:
                print(f"Invalid missiles '{missiles}' for {spell_name} given")
                return True

    def q(self):
        spell_name = "AhriOrbofDeception"
        tier = self.tiers['q']

        if self.invalid_tier_or_ap(self.tiers['q'], self.ap, spell_name): return None

        for value in self.response_data[f"Characters/{self.name_upper}/Spells/{spell_name}"]["mSpell"]["mDataValues"]:
            try:
                if value["mName"] == "BaseDamage": damages = value["mValues"][1:6]
            except KeyError: continue

        for value in self.response_data[f"Characters/{self.name_upper}/Spells/{spell_name}"]["mSpell"]["mSpellCalculations"]["TotalDamage"]["mFormulparts"]:
            try: 
                if value["mCoefficient"] is not None: scaling = value["mCoefficient"]
            except KeyError: continue

        return damages[tier - 1] + self.ap * scaling
    
    def w(self, missiles):
        spell_name = "AhriFoxFire"
        tier = self.tiers['w']

        if self.invalid_tier_or_ap(tier, self.ap, spell_name, missiles): return None

        for value in self.response_data[f"Characters/{self.name_upper}/Spells/{spell_name}"]["mSpell"]["mDataValues"]:
            try:
                if value["mName"] == "BaseDamage":      damages = value["mValues"][1:6]
                if value["mName"] == "RepeatDamageMod": damage_reduction = value["mValues"][1:6]
            except KeyError: continue

        for value in self.response_data[f"Characters/{self.name_upper}/Spells/{spell_name}"]["mSpell"]["mSpellCalculations"]["SingleFireDamage"]["mFormulaParts"]:
            try:
                if value["mCoefficient"] is not None: scaling = value["mCoefficient"]
            except KeyError: continue

        damage = 0
        for missile in range(1, missiles+1):
            ## first missile does full damage
            if missile == 1: damage += (damages[tier-1] + scaling * self.ap)
            ## second and third missile damage are reduced
            else:            damage += (damage_reduction[tier-1]*(damages[tier-1] + scaling * self.ap))

        return damage

    def e(self):
        spell_name = "AhriSeduce"
        tier = self.tiers['w']

        if self.invalid_tier_or_ap(tier, self.ap, spell_name): return None

        for value in self.response_data[f"Characters/{self.name_upper}/Spells/{spell_name}"]["mSpell"]["mDataValues"]:
            try:
                if value["mName"] == "BaseDamage": damages = value["mValues"][1:6]
                print(damages)
            except KeyError: continue

        for value in self.response_data[f"Characters/{self.name_upper}/Spells/{spell_name}"]["mSpell"]["mSpellCalculations"]["TotalDamage"]["mFormulaParts"]:
            try: 
                if value["mCoefficient"] is not None: scaling = value["mCoefficient"]
            except KeyError: continue

        return damages[tier - 1] + self.ap * scaling

    def r(self, missiles):
        spell_name = "AhriTumbleAbility/AhriTumble"
        tier = self.tiers['w']

        if self.invalid_tier_or_ap(tier, self.ap, spell_name, missiles, isUlt=True): return None

        for value in self.response_data[f"Characters/{self.name_upper}/Spells/{spell_name}"]["mSpell"]["mDataValues"]:
            try:
                if value["mName"] == "RBaseDamage":    damages = value["mValues"][1:4]
                if value["mName"] == "RAPCoefficient": scalings = value["mValues"][1:4]
            except KeyError: continue

        return (damages[tier-1] + scalings[tier-1] * self.ap) * missiles