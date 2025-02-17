import random


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
    
    def attack(self):
        return self.damage

    def add_experience(self, exp):
        self.experience+=exp
        if self.experience > (self.level+1)*100:
            print("You levelled up!")
            self.level+=1
            self.damage+=5
            self.health+=10

class Enemy:
    def __init__(self, enemy_class):
        self.enemy_class=enemy_class
        self.damage=random.randint(5, 15)
        self.health=random.randint(20,80)
        self.experience=0.5*self.health
        self.coins=random.randint(0, 3)

    def attack(self):
        return self.damage

class Boss:
    def __init__(self, enemy_class):
        self.enemy_class=enemy_class
        self.damage=random.randint(20, 40)
        self.health=random.randint(60, 100)
        self.experience=100
        self.coins=random.randint(10, 30)

    def attack(self):
        return self.damage

class RoomGenerator:
    def __init__(self):
        self.room_types=["Bedroom", "Chest", "Fight", "Shop", "Casino", "Story"]
        self.weights=[0.1, 0.1, 0.5, 0.1, 0.1, 0.1]

    def get_room(self):
        return random.choices(self.room_types,self.weights)[0]
    
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
        if current > len(self.chapters):
            return "No more chapters."
        return self.chapters[current]

class Chapter:
    def __init__(self,room_description,chapter_story):
        self.room_description=room_description
        self.chapter_story=chapter_story