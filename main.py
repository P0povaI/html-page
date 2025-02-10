import random
from classes import Player, Enemy, RoomGenerator, ChestGenerator


if __name__ == "__main__":
    p1 = Player(name="Ivan", player_class="Mage", damage=50)
    print(p1.name)
    print(p1.player_class)
    print(p1.health)
    print(p1.experience)
    print(p1.damage)
    room_generator = RoomGenerator()
    chest_generator = ChestGenerator()
    
    while True:
        current_room=room_generator.get_room()
        current_chest=chest_generator.get_loot()
        #current_action=
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
            #p1.experience+=20
            print("----- Chest -----")
            print("You entered a room and found a shiny chest! Type O to open it or type C to continue.")
            choice=input()
            if choice=="O":
                print("You opened it")
                if current_chest=="Health potion":
                    p1.health+=20
                    if p1.health>=100:
                        p1.health=100
                    print(f"You found a health potion. 20 health added.")
                    print("erorr1")
                elif current_chest=="Scroll":
                    p1.experience+=20
                    print(f"You found a scroll. 20 exp added.")
                    print("erorr2")
                elif current_chest=="Nothing":
                    print("You found nothing. Better luck next time!")
                    print("erorr3")
                elif current_room=="Explotion":
                    p1.health-=20
                    print("You lost 20 hp.Be more careful.")
                    print("erorr4")
            else:
                print("You moved to the next room!")
                print("erorr5")
                
            print(";_;")
            #print("You entered a room and found a shiny chest! Inside you found a book and now you have 20 experience")
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
    
                



        
