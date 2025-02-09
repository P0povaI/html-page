import random
from classes import Player, Enemy, RoomGenerator


if __name__ == "__main__":
    p1 = Player(name="Ivan", player_class="Mage", damage=50)
    print(p1.name)
    print(p1.player_class)
    print(p1.health)
    print(p1.experience)
    print(p1.damage)
    room_generator = RoomGenerator()
    while True:
        current_room=room_generator.get_room()
        if current_room=="Bedroom":
            print("----- Bedroom -----")
            print("You enter a bedroom!")
            if p1.coins<5:
                print("You don't have enough money to sleep! Move to the next room.")
            else:
                print("Do you want to take nap for 5 coins or countinue. Type N to take a nap or type C to continue.")
                nap=input()
                if nap=="N":
                    p1.coins-=5
                    p1.health = 100
                    print("You sleep and feel refreshed.")

            print(f"Health: {p1.health} Experience: {p1.experience}")
            print("-------------------\n")
        elif current_room=="Chest":
            p1.experience+=20
            print("----- Chest -----")
            print("The player entered a room and found a shiny chest! Inside you found a book and now you have 20 experience")
            print(f"Health: {p1.health} Experience: {p1.experience}")
            print("-------------------\n")
        elif current_room=="Fight":
            print("----- Fight -----")
            print("You entered a room and there is an enemy that attacks you!")
            enemy=Enemy(enemy_class="Skeleton",damage=random.randint(1,20),health=random.randint(20,80))
            print("You attacked the enemy!")
            while enemy.health>0:
                player_damage=p1.attack()
                enemy.health-=player_damage
                print(f"You deal: {player_damage} Enemy health: {enemy.health}")
                if enemy.health>0:
                    print("The enemy attacks you!")
                    enemy_damage=enemy.attack()
                    p1.health-=enemy_damage
                    print(f"The enemy deals {enemy_damage} Your health is {p1.health}")
                    if p1.health<=0:
                        print("You died!")
                        break
                else:
                    print("You killed the enemy!")
                    p1.experience+=enemy.experience
                    print(f"Player health: {p1.health} Player experience: {p1.experience}")
            print("-------------------\n")

        input("Press enter to continue...")
    
                



        
