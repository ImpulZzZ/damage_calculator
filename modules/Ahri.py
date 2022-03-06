import requests
import json
from modules.Data import Data

class Ahri():
    def __init__(self):
        self.name       = "ahri"
        self.name_upper = "Ahri"

        ## Fetch data from API
        data     = Data()
        url      = f"{data.base_url}/{data.patch}/game/data/characters/{self.name}/{self.name}.bin.json"
        response = requests.get(url)
        self.response_data = json.loads(response.text)


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

    
    def q(self, tier, ap):
        spell_name = "AhriOrbofDeception"

        if self.invalid_tier_or_ap(tier, ap, spell_name): return None

        for value in self.response_data[f"Characters/{self.name_upper}/Spells/{spell_name}"]["mSpell"]["mDataValues"]:
            try:
                if value["mName"] == "BaseDamage": damages = value["mValues"][1:6]
            except KeyError: continue

        for value in self.response_data[f"Characters/{self.name_upper}/Spells/{spell_name}"]["mSpell"]["mSpellCalculations"]["TotalDamage"]["mFormulaParts"]:
            try: 
                if value["mCoefficient"] is not None: scaling = value["mCoefficient"]
            except KeyError: continue

        return damages[tier - 1] + ap * scaling
    
    def w(self, tier, ap, missiles):
        spell_name = "AhriFoxFire"

        if self.invalid_tier_or_ap(tier, ap, spell_name, missiles): return None

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
            if missile == 1: damage += (damages[tier-1] + scaling * ap)
            ## second and third missile damage are reduced
            else:            damage += (damage_reduction[tier-1]*(damages[tier-1] + scaling * ap))

        return damage

    def e(self, tier, ap):
        spell_name = "AhriSeduce"

        if self.invalid_tier_or_ap(tier, ap, spell_name): return None

        for value in self.response_data[f"Characters/{self.name_upper}/Spells/{spell_name}"]["mSpell"]["mDataValues"]:
            try:
                if value["mName"] == "BaseDamage": damages = value["mValues"][1:6]
                print(damages)
            except KeyError: continue

        for value in self.response_data[f"Characters/{self.name_upper}/Spells/{spell_name}"]["mSpell"]["mSpellCalculations"]["TotalDamage"]["mFormulaParts"]:
            try: 
                if value["mCoefficient"] is not None: scaling = value["mCoefficient"]
            except KeyError: continue

        return damages[tier - 1] + ap * scaling

    def r(self, tier, ap, missiles):
        spell_name = "AhriTumbleAbility/AhriTumble"

        if self.invalid_tier_or_ap(tier, ap, spell_name, missiles, isUlt=True): return None

        for value in self.response_data[f"Characters/{self.name_upper}/Spells/{spell_name}"]["mSpell"]["mDataValues"]:
            try:
                if value["mName"] == "RBaseDamage":    damages = value["mValues"][1:4]
                if value["mName"] == "RAPCoefficient": scalings = value["mValues"][1:4]
            except KeyError: continue

        return (damages[tier-1] + scalings[tier-1] * ap) * missiles


        





