from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles


class NameModel(BaseModel):
    name: str

#class GameStatusModel(BaseModel):


app = FastAPI()

app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.post("/game/start")
def start_game():
    return "Start"

@app.post("/game/next_room")
def generate_room():
    return 0

@app.post("/game/final_boss")
def final_boss_fight():
    return 0

@app.post("/game/complete")
def game_completion():
    return choose_appropariate_name()

@app.post("/game/status")
def game_status(): #player stats
    return ";_<"

@app.post("/actions/fight/attack")
def fight():
    return 0

@app.post("/actions/fight/attack")
def fight():
    return 0
