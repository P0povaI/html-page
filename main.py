import random, math
from classes import Player, Enemy, RoomGenerator, ChestGenerator, StrategicRetreatGenerator, Boss
from storyline import story


if __name__ == "__main__":
    p1 = Player(name="Veti", player_class="Mage", damage=20)
    print(p1.name)
    print(p1.player_class)
    print(p1.health)
    print(p1.experience)
    print(p1.damage)
    print(p1.level)
    room_generator = RoomGenerator()
    chest_generator = ChestGenerator()
    strategic_retreat_generator = StrategicRetreatGenerator()
    while True:
        current_room=room_generator.get_room()
        current_chest=chest_generator.get_loot()
        current_action=strategic_retreat_generator.get_action()
        if current_room=="Casino":
            print("----- Casino -----")
            print("You enter a casino!")
            if p1.coins<1:
                print("You don't have enough money to bet! Move to the next room.")
            else:
                print("You can choose to bet some money.")
                print("You can either double or lose the money you bet.")
                print("Enter the amount of money you want to bet")
                bet=int(input())
                while bet>p1.coins:
                    print(f"You only have {p1.coins} coins. Enter a smaller amount.")
                    bet=int(input())
                print(f"You decided to bet {bet} coins.")
                outcomes=["Win", "Lose"]
                outcome_weights=[0.5, 0.5]
                outcome=random.choices(outcomes, outcome_weights)[0]
                if outcome=="Win":
                    p1.coins+=bet
                    print(f"Congratulations! You won {bet} coins!")
                else:
                    p1.coins-=bet
                    print(f"You are out of luck. You lost {bet} coins!")

            print(f"Health: {p1.health} Experience: {p1.experience} Player coins: {p1.coins}")
            print("-------------------\n")

        if current_room=="Bedroom":
            print("----- Bedroom -----")
            print("You enter a bedroom!")
            if p1.coins<5:
                print("You don't have enough money to sleep! Move to the next room.")
            else:
                print("Do you want to take nap for 5 coins or countinue. Type n to take a nap or type c to continue.")
                nap=input()
                if nap=="n":
                    p1.coins-=5
                    p1.health = p1.max_health
                    print("You sleep and feel refreshed.")

            print(f"Health: {p1.health} Experience: {p1.experience} Player coins: {p1.coins}")
            print("-------------------\n")
        elif current_room=="Chest":
            print("----- Chest -----")
            print("You entered a room and found a shiny chest! Type o to open it or type C to continue.")
            choice=input()
            if choice=="o":
                print("You opened it")
                if current_chest=="Health potion":
                    last_health=p1.health
                    p1.health+=20
                    if p1.health>=p1.max_health:
                        p1.health=p1.max_health
                    print(f"You found a health potion. {p1.health-last_health} health added.")
                elif current_chest=="Scroll":
                    p1.add_experience(20)
                    print(f"You found a scroll. 20 exp added.")
                elif current_chest=="Nothing":
                    print("You found nothing. Better luck next time!")
                elif current_chest=="Explosion":
                    p1.health-=20
                    if p1.health<=0:
                        print("You died!")
                        print(f"Player level:  Player kills: {p1.kills}")
                        exit()
                    else:
                        print("The chest exploded. You lost 20 hp.")
            else:
                print("You moved to the next room!")
                
            #print("You entered a room and found a shiny chest! Inside you found a book and now you have 20 experience")
            print(f"Health: {p1.health} Experience: {p1.experience} Player coins: {p1.coins}")
            print("-------------------\n")
        elif current_room=="Fight":
            print("----- Fight -----")
            enemies = ["enemy", "boss"]
            chances = [0.8, 0.2]
            enemy_type = random.choices(enemies, chances)[0]
            if enemy_type == "enemy":
                print("You entered a room and there is an enemy that attacks you!")
                enemy=Enemy(enemy_class="Skeleton")
            else:
                print("You entered a room and there is a mighty enemy waiting for you!")
                enemy=Boss(enemy_class="Dragon")
            print("You can choose fight or flight. Make your choice now f to fight and r to run away")
            action=input()
            if action=="f":
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
                            print(f"Player level:  Player kills: {p1.kills}")
                            exit()
                    else:
                        print("You killed the enemy!")
                        p1.add_experience(enemy.experience)
                        if enemy.coins>0:
                            p1.coins+=enemy.coins
                            print(f"You received: {enemy.coins} coins")
                        p1.kills+=1

                        
            elif action=="r":
                print("You choose to run away. >_<")
                print("You lost all your experience after the last time you levelled up.")
                p1.experience=p1.level*100
                if current_action=="hit":
                    print("Unlucky you got hit. You shoud run faster.")
                    print(f"The enemy deals {enemy.damage/2}")
                    p1.health-=enemy.damage/2
                else:
                    print("The enemy tried to hit you but missed.")

            print(f"Player health: {p1.health} Player experience: {p1.experience} Player coins: {p1.coins}")
            print("-------------------\n")

        elif current_room=="Shop":
            print("You came across a mysterious shop.")
            if p1.coins<15:
                print("You don't have enough money! Move to the next room.")
            else:
                print("You can update your damage or health.")
                print("d for damage and h for health - anything else for skip")
                item=input()
                if item=="d":
                    p1.damage+=1
                    p1.coins-=15
                    print(f"Your damage increased to: {p1.damage}")
                elif item=="h":
                    p1.health+=1
                    p1.coins-=15
                    print(f"Your health increased to: {p1.health}")
                else:
                    print("You didn't buy anything.")
            print(f"Player health: {p1.health} Player experience: {p1.experience} Player coins: {p1.coins}")
            print("-------------------\n")

        elif current_room=="Story":
            print("----- Story -----")
            chapter=story.return_next_chapter()
            print(chapter.room_description)
            print(chapter.chapter_story)
            print("-------------------\n")

        input("Press enter to continue...")

