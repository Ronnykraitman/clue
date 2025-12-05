import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
print("Starting server script...", flush=True)

try:
    from fastapi import FastAPI, HTTPException, WebSocket
    from fastapi.middleware.cors import CORSMiddleware
    from dotenv import load_dotenv
    print("Imports successful", flush=True)
except ImportError as e:
    print(f"Import failed: {e}", flush=True)
    sys.exit(1)

load_dotenv()


from src.clue.models import GameConfig, MoveRequest, SuspicionRequest, AccusationRequest, GameState, GamePhase
from src.clue.game_logic import ClueGame, ROOMS, WEAPONS, SUSPECTS
from src.clue.game_logic import ClueGame, ROOMS, WEAPONS, SUSPECTS

try:
    from src.clue.agents import ClueAI
except ImportError as e:
    print(f"WARNING: Could not import ClueAI: {e}", flush=True)
    ClueAI = None
except Exception as e:
    print(f"WARNING: Error importing ClueAI: {e}", flush=True)
    ClueAI = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game = ClueGame()
game = ClueGame()
try:
    ai_interface = ClueAI()
    print("AI Interface initialized successfully", flush=True)
except Exception as e:
    print(f"FAILED to initialize AI Interface: {e}", flush=True)
    ai_interface = None

@app.get("/")
async def root():
    return {"message": "Clue Game API"}

@app.post("/game/start")
async def start_game(config: GameConfig):
    state = game.initialize_game(config.human_character)
    return state

@app.get("/game/state")
async def get_state():
    if not game.state:
        raise HTTPException(status_code=400, detail="Game not started")
    return game.state

@app.post("/game/roll")
async def roll_dice():
    if not game.state:
        raise HTTPException(status_code=400, detail="Game not started")
    
    roll = game.roll_dice()
    current_player = game.state.players[game.state.current_player_index]
    valid_moves = game.get_valid_moves(current_player.position, roll)
    
    game.state.available_moves = valid_moves
    game.state.dice_rolled = True
    game.state.dice_rolled = True
    game.state.logs.append(f"{current_player.name} rolled a {roll}. Valid moves: {valid_moves}")
    
    if not valid_moves:
        game.state.logs.append(f"{current_player.name} has no valid moves. Staying in {current_player.position}.")
        game.state.phase = GamePhase.PLAYER_TURN_ACTION
    
    return {"roll": roll, "valid_moves": valid_moves}

@app.post("/game/move")
async def move(request: MoveRequest):
    if not game.state:
        raise HTTPException(status_code=400, detail="Game not started")
    
    game.move_player(game.state.current_player_index, request.destination_room)
    return game.state

@app.post("/game/suspect")
async def suspect(request: SuspicionRequest):
    if not game.state:
        raise HTTPException(status_code=400, detail="Game not started")
    
    result = game.handle_suspicion(request.suspect, request.weapon, request.room, game.state.current_player_index)
    game.next_turn() # End turn after suspicion (simplified flow)
    return {"state": game.state, "result": result}

@app.post("/game/accuse")
async def accuse(request: AccusationRequest):
    if not game.state:
        raise HTTPException(status_code=400, detail="Game not started")
    
    success = game.handle_accusation(request.suspect, request.weapon, request.room, game.state.current_player_index)
    if not success:
        game.next_turn()
    return {"state": game.state, "success": success}

@app.post("/game/pass")
async def pass_turn():
    if not game.state:
        raise HTTPException(status_code=400, detail="Game not started")
    
    game.next_turn()
    return game.state

@app.post("/game/ai-turn")
async def play_ai_turn():
    if not game.state:
        raise HTTPException(status_code=400, detail="Game not started")
    
    current_player = game.state.players[game.state.current_player_index]
    if current_player.is_human:
        raise HTTPException(status_code=400, detail="It is the human player's turn")
    
    # 1. Roll Dice
    roll = game.roll_dice()
    valid_moves = game.get_valid_moves(current_player.position, roll)
    game.state.logs.append(f"{current_player.name} rolled a {roll}.")
    
    # 2. Decide Move
    if valid_moves:
    # 2. Decide Move
    if valid_moves:
        if ai_interface:
            destination = ai_interface.decide_move(current_player, valid_moves, game.state)
        else:
            import random
            destination = random.choice(valid_moves)
            print("AI Interface not available, falling back to random move")
        
        game.move_player(game.state.current_player_index, destination)
    else:
        game.state.logs.append(f"{current_player.name} has no valid moves.")
        game.next_turn()
        return game.state

    # 3. Decide Action (Suspect)
    # AI will always try to suspect if in a room
    # (Simplified: AI doesn't Accuse yet to avoid early game over)
    # (Simplified: AI doesn't Accuse yet to avoid early game over)
    if ai_interface:
        suspicion = ai_interface.decide_suspicion(
            current_player, 
            current_player.position, 
            game.state, 
            SUSPECTS, 
            WEAPONS
        )
    else:
        # Fallback random suspicion
        import random
        suspicion = {
            "suspect": random.choice(SUSPECTS),
            "weapon": random.choice(WEAPONS),
            "room": current_player.position
        }
    
    result = game.handle_suspicion(
        suspicion["suspect"], 
        suspicion["weapon"], 
        suspicion["room"], 
        game.state.current_player_index
    )
    
    
    # 3.b Update AI Notebook based on suspicion result
    if result["has_card"]:
        # The game logic already updates 'seen_cards' and 'notebook' for the player 
        # inside handle_suspicion if a card is shown.
        pass
    else:
        # If no one could disprove, that's huge info!
        # It means the suspect, weapon, and room (that are not in my hand) are likely the answer.
        pass 
        # For now, simplistic notebook update is handled in game_logic, 
        # but complex deduction on 'pass' (no one showed) is implicit in 'unknowns' staying unknown.

    # 4. Decide Action (Accuse)
    # Now check if AI wants to accuse based on new info
    # 4. Decide Action (Accuse)
    # Now check if AI wants to accuse based on new info
    accusation = None
    if ai_interface:
        accusation = ai_interface.decide_accusation(current_player, game.state)
    
    if accusation:
        game.handle_accusation(
            accusation["suspect"],
            accusation["weapon"],
            accusation["room"],
            game.state.current_player_index
        )
        # Handle Accusation will either win (Game Over) or eliminate player
        # If eliminated, turn ends. If win, state updates to Game Over.
        
    if game.state.phase != GamePhase.GAME_OVER:
        game.next_turn()
    
    return game.state

@app.get("/game/constants")
async def get_constants():
    return {
        "rooms": ROOMS,
        "weapons": WEAPONS,
        "suspects": SUSPECTS
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.clue.server:app", host="0.0.0.0", port=8001, reload=True)

