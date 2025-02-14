import random
from classes import Player, Enemy, RoomGenerator, ChestGenerator, StrategicRetreatGenerator


if __name__ == "__main__":
    p1 = Player(name="Ivan", player_class="Mage", damage=50)
    print(p1.name)
    print(p1.player_class)
    print(p1.health)
    print(p1.experience)
    print(p1.damage)
    room_generator = RoomGenerator()
    chest_generator = ChestGenerator()
    strategic_retreat_generator = StrategicRetreatGenerator()
    while True:
        current_room=room_generator.get_room()
        current_chest=chest_generator.get_loot()
        current_action=strategic_retreat_generator.get_action()
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

            print(f"Health: {p1.health} Experience: {p1.experience} Player coins: {p1.coins}")
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
            print(f"Health: {p1.health} Experience: {p1.experience} Player coins: {p1.coins}")
            print("-------------------\n")
        elif current_room=="Fight":
            print("----- Fight -----")
            print("You entered a room and there is an enemy that attacks you!")
            enemy=Enemy(enemy_class="Skeleton",damage=random.randint(1,20),health=random.randint(20,80),coins=random.randint(0,3))
            print("You can choose fight or flight. Make your choice now f1 for fight and f2 for flight")
            action=input()
            if action=="f1":
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
                        p1.coins+=enemy.coins
                        
            elif action=="f2":
                print("You choose to run away. >_<")
                p1.experience-=p1.experience*0.20
                if current_action=="hit":
                    print("Unlucky you got hit. You shoud run faster.")
                    p1.health-=enemy.damage
            #remove 
            else:
                print("You choose to run away. >_<")
                p1.experience-=p1.experience*0.20
                if current_action=="hit":
                    print("Unlucky you got hit. You shoud run faster.")
                    p1.health-=enemy.damage


            print(f"Player health: {p1.health} Player experience: {p1.experience} Player coins: {p1.coins}")
            print("-------------------\n")

        elif current_room=="Shop":
            print("You came across a mysterious shop.")
            if p1.coins<35:
                print("You don't have enough money! Move to the next room.")
            else:
                print("You can update your damage or health.")
                print("d for damage and h for health - anything else for skip")
                item=input()
                if item=="d":
                    p1.damage+=1
                    p1.coins-=20
                    print("You feel stronger!")
                elif item=="h":
                    p1.health+=1
                    p1.coins-=15
                    print("You feel >^<")
                else:
                    print("You continued")
            print(f"Player health: {p1.health} Player experience: {p1.experience} Player coins: {p1.coins}")
            print("-------------------\n")

        input("Press enter to continue...")

