from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from classes import Player, RoomGenerator

class PlayerModel(BaseModel):
    name: str


#class GameStatusModel(BaseModel):


app = FastAPI()

app.mount("/static_assets", StaticFiles(directory="static", html=True), name="static_assets")

@app.get("/", response_class=FileResponse)
async def read_index():
    return "static/index.html"

@app.post("/game/start")
def start_game(params: PlayerModel):
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

@app.post("/game/next_room")
def generate_room():
    return 0

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
