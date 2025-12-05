import os
from textwrap import dedent
from typing import List, Dict, Any
from crewai import Agent, Task, Crew, Process
from src.clue.models import Player, GameState, Card

# Set OpenAI API Key from env if not already set (though it should be loaded)
# os.environ["OPENAI_API_KEY"] = ... 

class ClueAI:
    def __init__(self):
        self.agents_map = {}

    def create_agent(self, player: Player) -> Agent:
        if player.name in self.agents_map:
            return self.agents_map[player.name]

        # Define personality based on character
        personalities = {
            "Miss Scarlet": "Cunning, charming, and deceptive. You are a femme fatale who uses her wits to get what she wants.",
            "Colonel Mustard": "A dignified, dapper military man. You are pompous and somewhat blustery.",
            "Mrs. White": "A frazzled and intrusive housekeeper. You know all the secrets but try to appear innocent.",
            "Mr. Green": "A slick, smooth-talking businessman. You are always looking for an angle.",
            "Mrs. Peacock": "An elegant, socialite widow. You are proper, but have a sharp tongue.",
            "Professor Plum": "A quick-witted academic. You are arrogant and intellectual."
        }
        
        backstory = personalities.get(player.character_name, "A mysterious guest at the mansion.")

        agent = Agent(
            role=f"{player.character_name} (Clue Player)",
            goal="Win the game of Clue by deducing the murderer, weapon, and room.",
            backstory=dedent(f"""
                You are playing a game of Clue. 
                {backstory}
                Your objective is to figure out the solution cards (Room, Weapon, Suspect) held by the manager.
                You have a hand of cards and a notebook of information.
                Make logical deductions and try to mislead opponents if necessary.
            """),
            verbose=True,
            allow_delegation=False,
            # llm=... # Uses default OpenAI model from env
        )
        self.agents_map[player.name] = agent
        return agent

    def decide_move(self, player: Player, valid_moves: List[str], game_state: GameState) -> str:
        if not valid_moves:
            return None
        
        if len(valid_moves) == 1:
            return valid_moves[0]

        agent = self.create_agent(player)
        
        task_desc = dedent(f"""
            It is your turn to move.
            You are currently in {player.position}.
            You rolled the dice and can move to the following rooms: {', '.join(valid_moves)}.
            
            Your hand: {[c.name for c in player.hand]}
            Your notebook (known info): {player.notebook}
            
            Choose the best room to move to. 
            Consider:
            1. Rooms you haven't visited or need to investigate.
            2. Making a suspicion in a room to gather info.
            
            Return ONLY the name of the room you want to move to.
        """)

        task = Task(
            description=task_desc,
            agent=agent,
            expected_output="The name of the room to move to."
        )

        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential
        )

        result = crew.kickoff()
        
        # Simple parsing to ensure valid room
        chosen_room = str(result).strip()
        # Fallback if LLM is chatty
        for room in valid_moves:
            if room in chosen_room:
                return room
        return valid_moves[0] # Fallback to first valid move

    def decide_suspicion(self, player: Player, current_room: str, game_state: GameState, all_suspects: List[str], all_weapons: List[str]) -> Dict[str, str]:
        agent = self.create_agent(player)
        
        task_desc = dedent(f"""
            You are in the {current_room}.
            You need to make a suspicion to gather information.
            A suspicion consists of a Suspect and a Weapon. The Room is fixed to your current location ({current_room}).
            
            Your hand: {[c.name for c in player.hand]}
            Your notebook (known info): {player.notebook}
            
            Choose a Suspect and a Weapon to suspect.
            Strategy:
            - Don't suspect cards you hold in your hand (unless bluffing, but usually better to ask about unknowns).
            - Try to narrow down possibilities.
            
            Available Suspects: {', '.join(all_suspects)}
            Available Weapons: {', '.join(all_weapons)}
            
            Return your choice in the format: "Suspect: [Name], Weapon: [Name]"
        """)

        task = Task(
            description=task_desc,
            agent=agent,
            expected_output="String in format 'Suspect: [Name], Weapon: [Name]'"
        )

        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential
        )

        result = crew.kickoff()
        result_str = str(result)
        
        # Parse result
        chosen_suspect = None
        chosen_weapon = None
        
        for s in all_suspects:
            if s in result_str:
                chosen_suspect = s
                break
        for w in all_weapons:
            if w in result_str:
                chosen_weapon = w
                break
                
        # Fallbacks
        if not chosen_suspect: chosen_suspect = all_suspects[0]
        if not chosen_weapon: chosen_weapon = all_weapons[0]
        
        return {"suspect": chosen_suspect, "weapon": chosen_weapon, "room": current_room}

    def decide_accusation(self, player: Player, game_state: GameState) -> Dict[str, str]:
        # Deterministic Logic: Check notebook for elimination
        # If only 1 suspect, 1 weapon, and 1 room are unknown (not in notebook), ACCUSE!
        
        from src.clue.game_logic import SUSPECTS, WEAPONS, ROOMS
        
        unknown_suspects = [s for s in SUSPECTS if s not in player.notebook]
        unknown_weapons = [w for w in WEAPONS if w not in player.notebook]
        unknown_rooms = [r for r in ROOMS if r not in player.notebook]
        
        # Risk Taker Logic:
        # If the number of unknown combinations is small (e.g., <= 3), take a guess.
        # This speeds up the game as requested by the user.
        
        combinations = len(unknown_suspects) * len(unknown_weapons) * len(unknown_rooms)
        
        if combinations == 1:
            suspect = unknown_suspects[0]
            weapon = unknown_weapons[0]
            room = unknown_rooms[0]
            print(f"AI {player.name} is CERTAIN! Accusing: {suspect}, {weapon}, {room}")
            return {"suspect": suspect, "weapon": weapon, "room": room}
            
        elif combinations <= 3:
            import random
            suspect = random.choice(unknown_suspects) if unknown_suspects else SUSPECTS[0] # Fallback shouldn't happen if combinations > 0
            weapon = random.choice(unknown_weapons) if unknown_weapons else WEAPONS[0]
            room = random.choice(unknown_rooms) if unknown_rooms else ROOMS[0]
            
            print(f"AI {player.name} is taking a RISK (1 in {combinations} chance)! Accusing: {suspect}, {weapon}, {room}")
            return {"suspect": suspect, "weapon": weapon, "room": room}
            
        return None 
