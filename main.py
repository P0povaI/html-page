import random, math, time
from classes import Player, Enemy, RoomGenerator, ChestGenerator, StrategicRetreatGenerator, Boss , FinalBoss
from storyline import story


if __name__ == "__main__":
    p1 = Player(name="Veti", player_class="Mage", damage=20)
    print("\n-------------------------------")
    print(f"👤 Player name: {p1.name}")
    print(f"🧙‍♂️ Player class: {p1.player_class}")
    print(f"🧡 Player health: {p1.health}")
    print(f"🧠 Player experience: {p1.experience}")
    print(f"🗡️  Player damage: {p1.damage}")
    print(f"🎓 Player level: {p1.level}")
    print(f"💰 Player coins: {p1.coins}")
    print(f"👊 Player kills: {p1.kills}")
    print("-------------------------------\n")

    room_generator = RoomGenerator()
    chest_generator = ChestGenerator()
    strategic_retreat_generator = StrategicRetreatGenerator()
    while True:
        if story.current_chapter>len(story.chapters):
            enemy=FinalBoss()
            while enemy.health>0:
                time.sleep(1)
                player_damage=p1.attack()
                enemy.health-=player_damage
                print("|⚔️ You attacked the enemy!")
                print(f"|- You deal: {player_damage} damage. Enemy health: {enemy.health}\n|")
                if enemy.health>0:
                    print("|⚔️ The enemy attacks you!")
                    enemy_damage, enemy_effect=enemy.attack()
                    if enemy_effect:
                        p1.apply_effect(enemy_effect)
                    p1.health-=enemy_damage
                    print(f"|- The enemy deals {enemy_damage} damage. Your health is {p1.health}\n|")
                    if p1.health<=0:
                        print("😵 You died!")
                        print(f"🎓 Player level: {p1.level} 🗡️ Player kills: {p1.kills}")
                        exit()
                else:
                    print("\nYou killed the enemy!\n")
                    p1.add_experience(enemy.experience)
                    if enemy.coins>0:
                        p1.coins+=enemy.coins
                        print(f"🪙 You received: {enemy.coins} coins\n")
                    p1.kills+=1
        if p1.is_bleeding:
            p1.health-=5
            print("You are bleeding. You lose 5 hp. Buy a bandage to stop bleeding.")
            if p1.health<=0:
                print("😵 You died!")
                print(f"🎓 Player level: {p1.level} 🗡️ Player kills: {p1.kills}")
                exit()
        current_room, _ =room_generator.get_room()
        current_chest=chest_generator.get_loot()
        current_action=strategic_retreat_generator.get_action()

        if current_room=="Casino":
            print("------------ Gambling Hall ------------\n")
            print("🎰 You enter a gambling hall.")
            if p1.coins<1:
                print("You don't have enough money to bet! You continue to the next room.")
            else:
                print("You can choose to bet some money.")
                print("You can either double or lose the money you bet.")
                print("Enter the amount of money you want to bet")
                bet=int(input("Enter your choice: "))
                if bet == 0:
                    print("\nYou decided to not bet any money. You continue to the next room.\n")
                else:
                    while bet>p1.coins:
                        print(f"You only have {p1.coins} coins. Enter a smaller amount.")
                        bet=int(input("Enter your choice: "))
                    print(f"|💰 You decided to bet {bet} coins.\n|")
                    outcomes=["Win", "Lose"]
                    outcome_weights=[0.5, 0.5]
                    outcome=random.choices(outcomes, outcome_weights)[0]
                    if outcome=="Win":
                        p1.coins+=bet
                        print(f"|🎉 Congratulations! You won {bet} coins!\n|")
                    else:
                        p1.coins-=bet
                        print(f"|💔 You are out of luck. You lost {bet} coins!\n|")

            print(f"🧡 Health: {p1.health} 🧠 Experience: {p1.experience} 💰 Player coins: {p1.coins}")
            print("-------------------------------\n")
        elif current_room=="Bedroom":
            print("------------ Bedroom ------------\n")
            print("🛌 You enter a hall resembling an underground inn.")
            print("There is a strange man offering a bed for 5 coins.\n")
            if p1.coins<5:
                print("You don't have enough money to sleep! You continue to the next room.")
            else:
                print("🤔 Do you want to take the offer?")
                print("- Type 'n' to take a nap for 5 coins")
                print("- Type 'c' to continue\n")
                nap=input()
                if nap=="n":
                    p1.coins-=5
                    p1.health = p1.max_health
                    print("|😴 You take a nap and feel refreshed.\n")
                else:
                    print("You continue to the next room.\n")

            print(f"🧡 Health: {p1.health} 🧠 Experience: {p1.experience} 💰 Player coins: {p1.coins}")
            print("-------------------------------\n")
        elif current_room=="Chest":
            print("------------ Chest ------------\n")
            print("🤔 You entered a room and found a misterious chest. Do you want to open it?")
            print("- Type 'o' to open the chest")
            print("- Type 's' to skip the chest\n")
            choice=input("Enter your choice: ")
            if choice=="o":
                print("|👀 You open the chest\n|")
                if current_chest=="Health potion":
                    last_health=p1.health
                    p1.health+=20
                    if p1.health>=p1.max_health:
                        p1.health=p1.max_health
                    print(f"|🧪 You found a health potion. {p1.health-last_health} health added.\n")
                elif current_chest=="Scroll":
                    p1.add_experience(20)
                    print(f"|📖 You found a scroll. 20 exp added.\n")
                elif current_chest=="Nothing":
                    print("|💔 You found nothing. Better luck next time!\n")
                elif current_chest=="Explosion":
                    print("|💥 A trap! The chest exploded! You lose 20 health.\n")
                    p1.health-=20
                    if p1.health<=0:
                        print("😵 You died!")
                        print(f"🎓 Player level: {p1.level} 🗡️ Player kills: {p1.kills}")
                        exit()
            else:
                print("You decided not to open the chest and continue to the next room!\n")

            print(f"🧡 Health: {p1.health} 🧠 Experience: {p1.experience} 💰 Player coins: {p1.coins}")
            print("-------------------------------\n")
        elif current_room=="Fight":
            print("------------ Fight ------------\n")
            #print("💀 You entered a room and there is an enemy that attacks you!\n")
                #enemy=Enemy(enemy_class="Skeleton")
            
            enemies = ["enemy", "boss"]
            chances = [0.8, 0.2]
            enemy_type = random.choices(enemies, chances)[0]
            if enemy_type == "enemy":
                enemy=Enemy()
                enemy_class=enemy.enemy_class
                if enemy_class=="mage":
                    print("🧙🏻‍♀️ You entered a room and there is an enemy that attacks you!\n")
                    
                elif enemy_class=="fighter":
                    print("🥷🏻 You entered a room and there is an enemy that attacks you!\n")
                    
            else:
                print("🐲 You entered a room and there is a giant, powerful enemy waiting for you!\n")
                enemy=Boss(enemy_class="Dragon")
            time.sleep(1)
            print("🤔 You can choose to fight or run away. Make your choice now.")
            print("- Type 'f' to fight")
            print("- Type 'r' to run away\n")

            action=input("Enter your choice: ")

            if action=="f":
                while enemy.health>0:
                    time.sleep(1)
                    player_damage=p1.attack()
                    enemy.health-=player_damage
                    print("|⚔️ You attacked the enemy!")
                    print(f"|- You deal: {player_damage} damage. Enemy health: {enemy.health}\n|")
                    if enemy.health>0:
                        print("|⚔️ The enemy attacks you!")
                        enemy_damage, enemy_effect=enemy.attack()
                        if enemy_effect:
                            p1.apply_effect(enemy_effect)
                        p1.health-=enemy_damage
                        print(f"|- The enemy deals {enemy_damage} damage. Your health is {p1.health}\n|")
                        if p1.health<=0:
                            print("😵 You died!")
                            print(f"🎓 Player level: {p1.level} 🗡️ Player kills: {p1.kills}")
                            exit()
                    else:
                        print("\nYou killed the enemy!\n")
                        p1.add_experience(enemy.experience)
                        if enemy.coins>0:
                            p1.coins+=enemy.coins
                            print(f"🪙 You received: {enemy.coins} coins\n")
                        p1.kills+=1
            elif action=="r":
                print("|🏃 You choose to run away. >_<\n|")
                print("|💔 You lost all your experience after the last time you levelled up.\n|")
                p1.experience=p1.level*100
                if current_action=="hit":
                    print("|⚔️ As you try to run away, you got hit. You shoud run faster next time.")
                    print(f"|- The enemy deals {enemy.damage/2} damage.\n|")
                    p1.health-=enemy.damage/2
                    if p1.health<=0:
                        print("😵 You died!")
                        print(f"🎓 Player level: {p1.level} 🗡️ Player kills: {p1.kills}")
                        exit()
                else:
                    print("|💥 As you try to run away, the enemy tried to hit you but missed.\n|")

            print(f"🧡 Player health: {p1.health} 🧠 Player experience: {p1.experience} 💰 Player coins: {p1.coins}")
            print("-------------------------------\n")

        elif current_room=="Shop":
            print("------------ Shop ------------\n")
            print("🛠️ You came across a mysterious shop.\n")
            if p1.coins<15:
                print("You don't have enough money! You move to the next room.\n")
            else:
                print("🤔 You can update your damage or health. You can also buy the legendary Charm of Purity that grants the wearer the power to break free from any curse or The Hemostatic Bandage that quickly staunches bleeding, sealing wounds with its specially treated fabric. ")
                print("- Type 'd' to update your damage")
                print("- Type 'h' to update your health")
                print("- Type 'c' to buy charm")
                print("- Type 'b' to buy bandage")
                print("- Type anything else to skip\n")
                item=input("Enter your choice: ")
                if item=="d":
                    p1.damage+=2
                    p1.coins-=15
                    print(f"|🗡️ You spent 15 coins and your damage increased to: {p1.damage}\n")
                elif item=="h":
                    p1.max_health+=2
                    p1.coins-=15
                    print(f"|🧡 You spent 15 coins and your maximum health increased to: {p1.max_health}\n")
                elif item=="c":
                    p1.coins-=2
                    print(f"|🧿 You spent 30 coins and you broke free from the curse")
                    p1.remove_effect("curse")
                elif item=="b":
                    p1.coins-=2
                    print(f"|🩹 You spent 30 coins and you stopped the bleading")
                    p1.remove_effect("bleeding")
                else:
                    print("|💔 You didn't buy anything.\n|")
            print(f"🧡 Player health: {p1.health} 🧠 Player experience: {p1.experience} 💰 Player coins: {p1.coins}")
            print("-------------------------------\n")

        elif current_room=="Story":
            print("------------ Story ------------\n")
            chapter=story.return_next_chapter()
            try:
                print(chapter.room_description)
                print("\n")
                print(chapter.chapter_story)
                print("\n")
                print("-------------------------------\n")
            except:
                print("No more chapters")
        input("Press enter to continue...\n")

