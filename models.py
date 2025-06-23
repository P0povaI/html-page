from pydantic import BaseModel


class PlayerStartModel(BaseModel):
    name: str


class PlayerModel(BaseModel):
    name: str
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


class RoomModel(BaseModel):
    room_type: str
    room_description: str


class GameStartModel(BaseModel):
    player: PlayerModel
    room: RoomModel
