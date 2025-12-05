import random
from typing import List, Dict, Tuple, Optional
from src.clue.models import Card, CardType, GameState, Player, GamePhase

# Constants
ROOMS = [
    "Kitchen", "Ballroom", "Conservatory",
    "Dining Room", "Billiard Room", "Library",
    "Lounge", "Hall", "Study"
]

WEAPONS = [
    "Candlestick", "Dagger", "Lead Pipe",
    "Revolver", "Rope", "Wrench"
]

SUSPECTS = [
    "Miss Scarlet", "Colonel Mustard", "Mrs. White",
    "Mr. Green", "Mrs. Peacock", "Professor Plum"
]

# Simple adjacency for now (can be expanded with distances)
# This is a simplified map where rooms connect to neighbors.
# In a real board, there are hallways. For this version, we'll assume direct connections
# or a graph where nodes are rooms and edges have weights (steps).
# Let's define a simple distance matrix or graph.
BOARD_GRAPH = {
    "Kitchen": ["Ballroom", "Dining Room", "Study"], # Study via secret passage
    "Ballroom": ["Kitchen", "Conservatory", "Billiard Room", "Dining Room"],
    "Conservatory": ["Ballroom", "Billiard Room", "Lounge"], # Lounge via secret passage
    "Dining Room": ["Kitchen", "Ballroom", "Lounge", "Hall", "Billiard Room"], # Simplified connections
    "Billiard Room": ["Ballroom", "Conservatory", "Dining Room", "Library", "Hall"],
    "Library": ["Billiard Room", "Conservatory", "Study", "Hall"],
    "Lounge": ["Dining Room", "Hall", "Conservatory"], # Conservatory via secret passage
    "Hall": ["Dining Room", "Billiard Room", "Library", "Lounge", "Study"],
    "Study": ["Library", "Hall", "Kitchen"] # Kitchen via secret passage
}

# Distances between rooms (simplified for the sake of the example, 
# in a real grid board we'd calculate steps. Here we can assign arbitrary step costs)
# For now, let's say adjacent rooms are 3-4 steps away, others are further.
# Or we can just use the graph and say each hop is X steps.
# Let's stick to the prompt: "initialize the distance between each room (up to 12 steps)"
# We can pre-calculate or hardcode distances.
DISTANCES = {} 
# We will generate this dynamically or hardcode it. 
# For simplicity, let's assume a fully connected graph with weighted edges?
# No, the prompt implies a board structure.
# Let's use a BFS to calculate distances on the graph defined above, assuming each link is ~4 steps.

class ClueGame:
    def __init__(self):
        self.state = None
        self.truth = {}
        self.deck = []
        self.distances = self._calculate_distances()

    def _calculate_distances(self):
        # Simple BFS to find distances between all pairs of rooms
        dists = {r: {r2: 99 for r2 in ROOMS} for r in ROOMS}
        for r in ROOMS:
            dists[r][r] = 0
            queue = [(r, 0)]
            visited = set()
            while queue:
                curr, d = queue.pop(0)
                if curr in visited:
                    continue
                visited.add(curr)
                dists[r][curr] = min(dists[r][curr], d)
                
                # Neighbors are roughly 4 steps away in this simplified graph
                for neighbor in BOARD_GRAPH[curr]:
                    if neighbor not in visited:
                        queue.append((neighbor, d + 4))
        return dists

    def initialize_game(self, human_character: str):
        # 1. Create Deck
        cards = []
        for r in ROOMS: cards.append(Card(name=r, type=CardType.ROOM))
        for w in WEAPONS: cards.append(Card(name=w, type=CardType.WEAPON))
        for s in SUSPECTS: cards.append(Card(name=s, type=CardType.SUSPECT))
        
        random.shuffle(cards)

        # 2. Select Truth
        truth_room = next(c for c in cards if c.type == CardType.ROOM)
        truth_weapon = next(c for c in cards if c.type == CardType.WEAPON)
        truth_suspect = next(c for c in cards if c.type == CardType.SUSPECT)
        
        self.truth = {
            "room": truth_room,
            "weapon": truth_weapon,
            "suspect": truth_suspect
        }
        
        # Remove truth cards from deck
        cards.remove(truth_room)
        cards.remove(truth_weapon)
        cards.remove(truth_suspect)
        
        # 3. Create Players
        # Human player
        players = [Player(name="You", character_name=human_character, is_human=True, position="Lounge")]
        
        # AI Players
        ai_names = ["Sherlock", "Poirot", "Marple"]
        available_characters = [s for s in SUSPECTS if s != human_character]
        random.shuffle(available_characters)
        ai_characters = available_characters[:3]
        for i, char_name in enumerate(ai_characters):
            name = ai_names[i] if i < len(ai_names) else f"AI_{i+1}"
            players.append(Player(name=name, character_name=char_name, is_human=False, position="Lounge"))
            
        # 4. Deal Cards (4 per player)
        random.shuffle(cards)
        for player in players:
            for _ in range(4):
                if cards:
                    card = cards.pop()
                    player.hand.append(card)
                    # Mark own cards in notebook
                    player.notebook[card.name] = "HAND"
        
        # Remaining cards are hidden (known only to manager - effectively removed from play for players)
        
        self.state = GameState(
            players=players,
            current_player_index=0,
            phase=GamePhase.PLAYER_TURN_MOVE,
            logs=["Game initialized. All players at Lounge."]
        )
        
        return self.state

    def roll_dice(self) -> int:
        return random.randint(1, 6) + random.randint(1, 6)

    def get_valid_moves(self, current_room: str, dice_roll: int) -> List[str]:
        valid_rooms = []
        for room, distance in self.distances[current_room].items():
            if 0 < distance <= dice_roll:
                valid_rooms.append(room)
        return valid_rooms

    def move_player(self, player_index: int, destination: str):
        self.state.players[player_index].position = destination
        self.state.logs.append(f"{self.state.players[player_index].name} moved to {destination}")
        self.state.phase = GamePhase.PLAYER_TURN_ACTION

    def handle_suspicion(self, suspect: str, weapon: str, room: str, player_index: int):
        # Move suspect to room
        for p in self.state.players:
            if p.character_name == suspect:
                p.position = room
                self.state.logs.append(f"{suspect} was moved to {room}")
        
        self.state.logs.append(f"{self.state.players[player_index].name} suspects {suspect} with {weapon} in {room}")
        
        # Check if other players have matching cards
        # Start from next player
        num_players = len(self.state.players)
        for i in range(1, num_players):
            check_idx = (player_index + i) % num_players
            checker = self.state.players[check_idx]
            
            matches = [c for c in checker.hand if c.name in [suspect, weapon, room]]
            if matches:
                shown_card = random.choice(matches) # AI logic: show random match
                self.state.logs.append(f"{checker.name} showed a card to {self.state.players[player_index].name}")
                
                # Record seen card for the player who made the suspicion
                # Record seen card for the player who made the suspicion
                if shown_card.name not in self.state.players[player_index].seen_cards:
                    self.state.players[player_index].seen_cards.append(shown_card.name)
                    # Update notebook
                    self.state.players[player_index].notebook[shown_card.name] = "SEEN"
                
                return {"has_card": True, "player": checker.name, "card": shown_card if self.state.players[player_index].is_human else None}
        
        self.state.logs.append("No one could disprove the suspicion.")
        
        # Record this valuable info for the player
        undisproved = {"suspect": suspect, "weapon": weapon, "room": room}
        self.state.players[player_index].undisproved_suspicions.append(undisproved)
        
        return {"has_card": False}

    def handle_accusation(self, suspect: str, weapon: str, room: str, player_index: int):
        is_correct = (
            suspect == self.truth["suspect"].name and
            weapon == self.truth["weapon"].name and
            room == self.truth["room"].name
        )
        
        if is_correct:
            self.state.winner = self.state.players[player_index].name
            self.state.phase = GamePhase.GAME_OVER
            self.state.logs.append(f"{self.state.players[player_index].name} WON! Correct accusation: {suspect}, {weapon}, {room}")
            return True
        else:
            self.state.players[player_index].is_eliminated = True
            self.state.logs.append(f"{self.state.players[player_index].name} made a false accusation and is eliminated.")
            return False

    def next_turn(self):
        # Find next active player
        start_idx = self.state.current_player_index
        while True:
            self.state.current_player_index = (self.state.current_player_index + 1) % len(self.state.players)
            if not self.state.players[self.state.current_player_index].is_eliminated:
                break
            if self.state.current_player_index == start_idx:
                # All players eliminated? Should not happen usually unless everyone guessed wrong
                self.state.phase = GamePhase.GAME_OVER
                self.state.logs.append("All players eliminated. Game Over.")
                return

        self.state.phase = GamePhase.PLAYER_TURN_MOVE
        self.state.dice_rolled = False
        self.state.logs.append(f"It is {self.state.players[self.state.current_player_index].name}'s turn.")
