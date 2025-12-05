from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel

class CardType(str, Enum):
    SUSPECT = "suspect"
    WEAPON = "weapon"
    ROOM = "room"

class Card(BaseModel):
    name: str
    type: CardType

class Position(BaseModel):
    room_name: str
    # We might need coordinates for the UI, but logical position is just the room

class Player(BaseModel):
    name: str
    character_name: str
    hand: List[Card] = []
    position: str  # Room name
    is_human: bool = False
    is_eliminated: bool = False
    notebook: Dict[str, str] = {} # Card name -> status (e.g., "X", "?", "OK")
    seen_cards: List[str] = [] # Cards shown to this player
    undisproved_suspicions: List[Dict[str, str]] = [] # [{suspect: X, weapon: Y, room: Z}]

class GamePhase(str, Enum):
    SETUP = "setup"
    PLAYER_TURN_MOVE = "player_turn_move"
    PLAYER_TURN_ACTION = "player_turn_action" # Suspect, Accuse, Pass
    GAME_OVER = "game_over"

class GameState(BaseModel):
    players: List[Player]
    current_player_index: int
    phase: GamePhase
    winner: Optional[str] = None
    logs: List[str] = []
    # The board structure might be static, so maybe not needed in state, 
    # but available moves could be useful
    available_moves: List[str] = [] 
    dice_rolled: bool = False 

class MoveRequest(BaseModel):
    destination_room: str

class SuspicionRequest(BaseModel):
    suspect: str
    weapon: str
    room: str # Must be current room

class AccusationRequest(BaseModel):
    suspect: str
    weapon: str
    room: str

class GameConfig(BaseModel):
    human_character: str
