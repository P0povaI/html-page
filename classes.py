import random
from clients import generate_story


def create_template_player():
    player=Player(name="Player", player_class="Knight", damage=10)
    return player

class Player:
    def __init__(self, name, player_class, damage):
        self.name = name
        self.player_class = player_class
        self.max_health = 100
        self.health = 100
        self.experience = 0
        self.damage = damage
        self.coins = 10
        self.level=0
        self.kills=0
        self.is_cursed=False
        self.is_bleeding=False

    def update_from_existing_player(self, player):
        self.name=player.name
        self.player_class=player.player_class
        self.max_health=player.max_health
        self.health=player.health
        self.experience=player.experience
        self.damage=player.damage_base
        self.coins=player.coins
        self.level=player.level
        self.kills=player.kills
        self.is_cursed=player.is_cursed
        self.is_bleeding=player.is_bleeding

    def return_player_model_vars(self):
        return {
            "name": self.player_name,
            "player_class": self.player_class,
            "health": self.health,
            "max_health": self.max_health,
            "experience": self.experience,
            "level": self.level,
            "damage_base": int(self.damage_base),
            "coins": int(self.coins),
            "kills": int(self.kills),
            "is_cursed": bool(self.is_cursed),
            "is_bleeding": bool(self.is_bleeding)   
        }

    def attack(self):
        if self.is_cursed:
            print("You are cursed and you deal less damage.")
            return self.damage*0.8
        
        return self.damage

    def add_experience(self, exp):
        self.experience+=exp
        if self.experience > (self.level+1)*100:
            print("You levelled up!")
            self.level+=1
            self.damage+=5
            self.health+=10

    def apply_effect(self,effect):
        if effect=="curse":
            self.is_cursed=True
            print("The enemy cursed you!")

        elif effect=="bleeding":
            self.is_bleeding=True
            print("The enemy made you bleed!")

    def remove_effect(self,effect):
        if effect=="curse":
            self.is_cursed=False
        elif effect=="bleeding":
            self.is_bleeding=False

class Enemy:
    EFFECTS={"mage": "curse", "fighter": "bleeding"}
    def __init__(self):
        self.damage=random.randint(5, 15)
        self.health=random.randint(20,80)
        self.experience=0.5*self.health
        self.coins=random.randint(0, 3)
        self.enemy_classes_types=["mage", "fighter"]
        self.chance_of_encounter=[0.5, 0.5]
        self.enemy_class = random.choices(self.enemy_classes_types,self.chance_of_encounter)[0]


    def attack(self):
        self.effect_type=[self.EFFECTS[self.enemy_class], None]
        self.effect_chance=[0.5,0.5]
        return self.damage, random.choices(self.effect_type,self.effect_chance)[0]


class Boss:
    def __init__(self, enemy_class):
        self.enemy_class=enemy_class
        self.damage=random.randint(20, 40)
        self.health=random.randint(60, 100)
        self.experience=100
        self.coins=random.randint(10, 30)

    def attack(self):
        return self.damage, None

class RoomGenerator:
    def __init__(self):
        self.room_types=["Bedroom", "Chest", "Fight", "Shop", "Casino", "Story"]
        self.weights=[0.1, 0.1, 0.1, 0.1, 0.1, 0.5]
        self.descriptions={
        "Bedroom": "🛌 You enter a hall resembling an underground inn.\n There is a strange man offering a bed for 5 coins.\n",
        "Chest": "🤔 You entered a room and found a misterious chest. Do you want to open it?",
        "Fight": "💀 You entered a room and there is an enemy that attacks you!\n",
        "Shop": "🛠️ You came across a mysterious shop.\n",
        "Casino": "🎰 You enter a gambling hall.",
        "Story": ""
    }

    def get_room(self):
        room_type = random.choices(self.room_types,self.weights)[0]
        room_description=self.descriptions[room_type]
        return room_type, room_description
    
class ChestGenerator:
    def __init__(self):
        self.loot_types=["Health potion", "Scroll", "Nothing", "Explosion"]
        self.weights=[0.2,0.2,0.4,0.2]
    
    def get_loot(self):
        return random.choices(self.loot_types,self.weights)[0]

#change name to HitOrMiss
class StrategicRetreatGenerator:
    def __init__(self):
        self.action_types=["hit","miss"]
        self.weights=[0.5,0.5]

    def get_action(self):
        return random.choices(self.action_types,self.weights)[0]

class Storyline:
    def __init__(self,chapters):
        self.chapters=chapters
        self.current_chapter=0
        

    def return_next_chapter(self):
        current=self.current_chapter
        self.current_chapter+=1
        if current > len(self.chapters)-1:
            return "No more chapters."
        return self.chapters[current]
    
    

class Chapter:
    def __init__(self,room_description,chapter_story):
        self.room_description=room_description
        self.chapter_story=chapter_story

class FinalBoss:
    EFFECTS={"mage": "curse", "fighter": "bleeding"}
    def __init__(self):
        self.name="Xarathor, the Infinite Harbinger"
        self.enemy_class="Final boss"
        self.damage=50
        self.health=150
        self.experience=200
        self.coins=100

    def attack(self):
        return self.damage, "curse"
        
