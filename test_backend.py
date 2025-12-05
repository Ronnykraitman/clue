import requests
import time

BASE_URL = "http://localhost:8001"

def test_game_flow():
    # 1. Start Game
    print("Starting game...")
    response = requests.post(f"{BASE_URL}/game/start", json={"human_character": "Miss Scarlet"})
    if response.status_code != 200:
        print(f"Failed to start game: {response.text}")
        return
    state = response.json()
    print("Game started. Players:", [p['name'] for p in state['players']])

    # 2. Get State
    response = requests.get(f"{BASE_URL}/game/state")
    assert response.status_code == 200
    print("State retrieved successfully.")

    # 3. Roll Dice (Human turn)
    print("Rolling dice...")
    response = requests.post(f"{BASE_URL}/game/roll")
    if response.status_code == 200:
        data = response.json()
        print(f"Rolled: {data['roll']}, Valid moves: {data['valid_moves']}")
        
        # 4. Move (if moves available)
        if data['valid_moves']:
            move_to = data['valid_moves'][0]
            print(f"Moving to {move_to}...")
            response = requests.post(f"{BASE_URL}/game/move", json={"destination_room": move_to})
            assert response.status_code == 200
            print("Moved successfully.")
            
            # 5. Pass (end turn)
            print("Passing turn...")
            requests.post(f"{BASE_URL}/game/pass")
        else:
            print("No moves, passing...")
            requests.post(f"{BASE_URL}/game/pass")

    # 6. AI Turn
    print("Triggering AI turn...")
    response = requests.post(f"{BASE_URL}/game/ai-turn")
    if response.status_code == 200:
        print("AI turn completed.")
        state = response.json()
        print("Logs:", state['logs'][-2:])
    else:
        print(f"AI turn failed: {response.text}")

if __name__ == "__main__":
    try:
        test_game_flow()
    except Exception as e:
        print(f"Test failed: {e}")
