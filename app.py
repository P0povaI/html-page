from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from classes import Player, RoomGenerator, ChestGenerator, Enemy, Boss, StrategicRetreatGenerator
from storyline import story
import random

class PlayerStartModel(BaseModel):
    name: str

class PlayerModel(BaseModel):
    name: str
    player_class: str
    health: int
    max_health: int
    experience: int
    level: int
    damage_base: int
    coins: int
    kills: int
    is_cursed: bool
    is_bleeding: bool

class EnemyModel(BaseModel):
    enemy_class: str
    enemy_type: str
    damage: int
    health: int
    experience: float
    coins: int

class CasinoModel(BaseModel):
    bet: int
    player: PlayerModel

class MarketplaceModel(BaseModel):
    item: str
    player: PlayerModel

class ChestModel(BaseModel):
    player: PlayerModel

class BedroomModel(BaseModel):
    player: PlayerModel

class FightAttackModel(BaseModel):
    player: PlayerModel
    enemy: EnemyModel

class FightRunModel(BaseModel):
    player: PlayerModel
    enemy: EnemyModel

class ActionResult(BaseModel):
    player: PlayerModel
    result: str

#class GameStatusModel(BaseModel):

catalog_items={"bandage": 30, "charm": 30, "health_potion":15, "strength_potion": 15}
bedroom_option={"sleep": 5}

app = FastAPI()

app.mount("/static_assets", StaticFiles(directory="static", html=True), name="static_assets")

@app.get("/", response_class=FileResponse)
async def read_index():
    return "static/index.html"

@app.post("/game/start")
def start_game(params: PlayerStartModel):
    player = Player(params.name, player_class="Mage", damage=20)
    room_generator = RoomGenerator()
    room, description = room_generator.get_room()
    return {
        "player": {
            "name": player.name,
            "player_class": player.player_class,
            "health": player.health,
            "max_health": player.max_health,
            "experience": player.experience,
            "level": player.level,
            "damage_base": player.damage,
            "coins": player.coins,
            "kills": player.kills,
            "is_cursed": player.is_cursed,
            "is_bleeding": player.is_bleeding
        },
        "room":{
            "room_type": room,
            "room_description": description
        }
        }

@app.get("/game/next_room")
def generate_room():
    room_generator = RoomGenerator()
    room, description = room_generator.get_room()
    if room == "Story":
        chapter=story.return_next_chapter()
        description=f"{chapter.room_description}\n{chapter.chapter_story}"
    return {
        "room":{
            "room_type": room,
            "room_description": description
        }
        }

@app.get("/fight/enemy")
def get_enemy():
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
    return EnemyModel(enemy_class=enemy.enemy_class, enemy_type=enemy_type, damage= enemy.damage, health= enemy.health, experience= enemy.experience, coins= enemy.coins)

@app.post("/actions/casino/bet")
def casino(params: CasinoModel):
    outcomes=["Win", "Lose"]
    outcome_weights=[0.5, 0.5]
    outcome=random.choices(outcomes, outcome_weights)[0]
    if outcome=="Win":
        params.player.coins+=params.bet
        bet_result=f"|🎉 Congratulations! You won {params.bet} coins!\n|"
    else:
        params.player.coins-=params.bet
        bet_result=f"|💔 You are out of luck. You lost {params.bet} coins!\n|"
    return ActionResult(player=params.player, result=bet_result)

@app.post("/actions/marketplace/purchase")
def marketplace(params: MarketplaceModel):
    
    price= catalog_items[params.item]
    if params.item=="strength_potion":
        params.player.damage_base+=2
        market_result=f"|🗡️ You spent {price} coins and your damage increased to: {params.player.damage_base}\n"
    elif params.item=="health_potion":
        params.player.max_health+=2
        market_result=f"|🧡 You spent {price} coins and your maximum health increased to: {params.player.max_health}\n"
    elif params.item=="charm":
        market_result=f"|🧿 You spent {price} coins and you broke free from the curse"
        params.player.is_cursed=False
    elif params.item=="bandage":
        market_result=f"|🩹 You spent {price} coins and you stopped the bleading"
        params.player.is_bleeding=False
    params.player.coins-=price
    return ActionResult(player= params.player, result= market_result)

@app.get("/marketplace/catalog")
def catalog():
    return catalog_items

@app.post("/actions/chest/open")
def chest(params: ChestModel):
    chest_generator=ChestGenerator()
    outcome=chest_generator.get_loot()
    if outcome=="Health potion":
        #last_health=params.player.health
        #healed=params.player.health+20
        #if params.player.health>=params.player.max_health:
        #params.player.health=params.player.max_health
        #chest_result=f"|🧪 You found a health potion. {abs(healed-last_health)} health added.\n"
        last_health = params.player.health
        params.player.health = min(params.player.health + 20, params.player.max_health)
        healed = params.player.health - last_health
        chest_result = f"|🧪 You found a health potion. {healed} health added.\n"

    elif outcome=="Scroll":
        params.player.experience+=20
        chest_result=f"|📖 You found a scroll. 20 exp added.\n"
    elif outcome=="Nothing":
        chest_result=f"|💔 You found nothing. Better luck next time!\n"
    elif outcome=="Explosion":
        params.player.health-=20
        if params.player.health<=0:
            chest_result="😵 You died!"
            chest_result+=f"🎓 Player level: {params.player.level} 🗡️ Player kills: {params.player.kills}"
        else:
            chest_result=f"|💥 A trap! The chest exploded! You lose 20 health.\n"
    return ActionResult(player=params.player, result= chest_result)    

@app.post("/actions/bedroom/sleep")
def bedroom(params: BedroomModel):
    params.player.coins-=bedroom_option["sleep"]
    params.player.health = params.player.max_health
    bedroom_result="|😴 You take a nap and feel refreshed.\n" 
    return ActionResult(player= params.player, result= bedroom_result)

@app.get("/bedroom/options")
def bedroom_op():
    return bedroom_option

@app.post("/actions/fight/attack")
def fight_attack(params: FightAttackModel):
    enemy=params.enemy
    p1=Player(params.player.name, params.player.player_class, params.player.damage_base)
    while enemy.health>0:
        player_damage=p1.attack()
        enemy.health-=player_damage
        fight_attack_result="|⚔️ You attacked the enemy!"
        fight_attack_result+=f"|- You deal: {player_damage} damage. Enemy health: {enemy.health}\n|"
        if enemy.health>0:
            fight_attack_result="|⚔️ The enemy attacks you!"
            enemy_damage, enemy_effect=enemy.attack()
            if enemy_effect:
                p1.apply_effect(enemy_effect)
            p1.health-=enemy_damage
            fight_attack_result=f"|- The enemy deals {enemy_damage} damage. Your health is {p1.health}\n|"
            if p1.health<=0:
                fight_attack_result="😵 You died!"
                fight_attack_result+=f"🎓 Player level: {p1.level} 🗡️ Player kills: {p1.kills}"
        else:
            fight_attack_result="\nYou killed the enemy!\n"
            p1.add_experience(enemy.experience)
            if enemy.coins>0:
                p1.coins+=enemy.coins
                fight_attack_result=f"🪙 You received: {enemy.coins} coins\n"
            p1.kills+=1
    return 0

@app.post("/actions/fight/run")
def fight_run(params: FightRunModel):
    fight_run_result="|🏃 You choose to run away. >_<\n|" + "|💔 You lost all your experience after the last time you levelled up.\n|"
    params.player.experience=params.player.level*100
    strategicRetreat=StrategicRetreatGenerator()
    current_action=strategicRetreat.get_action()
    if current_action=="hit":
        fight_run_result+="\n|⚔️ As you try to run away, you got hit. You shoud run faster next time." + f"|- The enemy deals {params.enemy.damage/2} damage.\n|"
        params.player.health-=params.enemy.damage/2
        if params.player.health<=0:
            fight_run_result+="\n😵 You died!" + f"🎓 Player level: {params.player.level} 🗡️ Player kills: {params.player.kills}"
    else:
        fight_run_result+="\n|💥 As you try to run away, the enemy tried to hit you but missed.\n|"
    return ActionResult(player= params.player, result= fight_run_result)

@app.post("/game/final_boss")
def final_boss_fight():
    return 0

@app.post("/game/complete")
def game_completion():
    return 0

@app.post("/game/status")
def game_status(): #player stats
    return ";_<"

@app.post("/actions/fight/attack")
def fight():
    return 0
