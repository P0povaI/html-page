import random


class Player:
    def __init__(self, name, player_class, damage):
        self.name = name
        self.player_class = player_class
        self.health = 100
        self.experience = 0
        self.damage = damage
        self.coins = 10
    
    def attack(self):
        return self.damage

class Enemy:
    def __init__(self, enemy_class, damage, health, coins):
        self.enemy_class=enemy_class
        self.damage=damage
        self.health=health
        self.experience=2*self.health
        self.coins=coins

    def attack(self):
        return self.damage    

class RoomGenerator:
    def __init__(self):
        self.room_types=["Bedroom","Chest","Fight","Shop"]#Shop-Trashbin
        self.weights=[0.1,0.2,0.6,0.1]

    def get_room(self):
        return random.choices(self.room_types,self.weights)[0]
    
class ChestGenerator:
    def __init__(self):
        self.loot_types=["Health potion","Scroll","Nothing","Explotion"]
        self.weights=[0.2,0.2,0.4,0.2]
    
    def get_loot(self):
        return random.choices(self.loot_types,self.weights)[0]
    #def open_chest(self):
        #return self

#change name to HitOrMiss
class StrategicRetreatGenerator:
    def __init__(self):
        self.action_types=["hit","miss"]
        self.weights=[0.5,0.5]

    def get_action(self):
        return random.choices(self.action_types,self.weights)[0]