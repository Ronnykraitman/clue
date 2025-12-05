# Clue AI: The Mystery 🕵️‍♂️🔍

Welcome to **Clue AI**, a modern web-based adaptation of the classic detective board game, enhanced with intelligent AI opponents. Test your deduction skills against legendary detectives like Sherlock, Poirot, and Marple, powered by advanced AI logic.

## 🌟 Features

*   **Interactive Gameplay**: Move across the classic mansion board, roll the dice, and investigate rooms.
*   **Intelligent AI Agents**: Play against AI characters that use logic, memory, and deduction to track cards, make suspicions, and even take risky accusations when they are close to solving the case.
*   **Smart Notebook**: Automatically tracks your hand, cards you've seen, and—crucially—**undisproved suspicions**, giving you a tactical edge.
*   **Immersive UI**: A Victorian-themed interface with a wooden board, verified character portraits, and atmospheric styling.
*   **Single Player Mode**: Challenge 3 AI opponents in a race to solve the murder.

## 🛠️ Technology Stack

*   **Frontend**: React, Vite, CSS3 (Custom Design System).
*   **Backend**: Python, FastAPI.
*   **AI Logic**: Custom agent logic using CrewAI/LLM integration (simulated/implemented) for personality and deduction.

## 🚀 Getting Started

### Prerequisites

*   Python 3.8+
*   Node.js 16+
*   npm or yarn

### Installation & Running

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd clue
    ```

2.  **Start the Backend Server**
    ```bash
    # It is recommended to create a virtual environment first
    # python3 -m venv venv
    # source venv/bin/activate
    
    python3 src/clue/server.py
    ```
    The server will start on `http://0.0.0.0:8001`.

3.  **Start the Frontend Application**
    Open a new terminal window:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```
    The game should now be accessible at the URL provided by Vite (usually `http://localhost:5173`).

## 🎮 How to Play

1.  **Select Your Character**: Choose from the classic cast: Miss Scarlet, Colonel Mustard, Mrs. White, Mr. Green, Mrs. Peacock, or Professor Plum.
2.  **Roll & Move**: On your turn, roll the dice to see which rooms are within reach.
3.  **Suspect**: Enter a room and make a **Suspicion** (suggest a Suspect and Weapon).
    *   If another player stands in your way, they must show you one card that disproves your theory.
    *   If *no one* can disprove it, the suspicion is logged in your notebook as a potential solution!
4.  **Accuse**: Once you are confident, make an **Accusation**. Be careful—if you are wrong, you are eliminated!

## 🤖 AI Behavior

The AI agents aren't just random movers. They:
*   Maintain their own private notebooks.
*   Remember cards shown to them.
*   Will make an accusation if they narrow the possibilities down to 1 (100% certainty) or even take a calculated risk if only a few options remain (33% chance).

## 📄 License

This project is for educational and entertainment purposes.

---
*Created with ❤️ by the Clue AI Team.*
