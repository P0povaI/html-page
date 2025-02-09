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
    def __init__(self, enemy_class, damage, health):
        self.enemy_class=enemy_class
        self.damage=damage
        self.health=health
        self.experience=2*self.health
    
    def attack(self):
        return self.damage

class RoomGenerator:
    def __init__(self):
        self.room_types=["Bedroom","Chest","Fight"]
        self.weights=[0.1,0.2,0.7]

    def get_room(self):
        return random.choices(self.room_types,self.weights)[0]