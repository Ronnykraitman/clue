import React, { useState, useEffect, useRef } from 'react';
import { api } from './api';
import Board from './components/Board';
import GameControls from './components/GameControls';
import Notebook from './components/Notebook';
import Hand from './components/Hand';
import PlayersList from './components/PlayersList';
import './App.css';
import RulesModal from './components/RulesModal';
import VictoryModal from './components/VictoryModal';

function App() {
    const [gameState, setGameState] = useState(null);
    const [constants, setConstants] = useState({ rooms: [], weapons: [], suspects: [] });
    const [humanCharacter, setHumanCharacter] = useState(null);
    const [gameStarted, setGameStarted] = useState(false);
    const [loading, setLoading] = useState(false);
    const [showRules, setShowRules] = useState(false);
    const logsEndRef = useRef(null);

    const scrollToBottom = () => {
        logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [gameState?.logs]);

    useEffect(() => {
        api.getConstants().then(res => setConstants(res.data));
    }, []);

    const startGame = async (character) => {
        setLoading(true);
        try {
            const res = await api.startGame(character);
            setGameState(res.data);
            setHumanCharacter(character);
            setGameStarted(true);
        } catch (err) {
            console.error("Failed to start game", err);
        }
        setLoading(false);
    };

    const refreshState = async () => {
        try {
            const res = await api.getState();
            setGameState(res.data);
        } catch (err) {
            console.error("Failed to get state", err);
        }
    };

    // Poll for state updates or handle AI turns
    useEffect(() => {
        if (!gameStarted || !gameState) return;

        const currentPlayer = gameState.players[gameState.current_player_index];
        if (!currentPlayer.is_human && !gameState.winner) {
            // AI Turn
            const timer = setTimeout(async () => {
                try {
                    const res = await api.playAiTurn();
                    setGameState(res.data);
                } catch (err) {
                    console.error("AI turn failed", err);
                }
            }, 2000); // Delay for visual effect
            return () => clearTimeout(timer);
        }
    }, [gameState, gameStarted]);

    if (!gameStarted) {
        return (
            <div className="start-screen">
                <h1>Clue Ai<br /><span className="subtitle-main">The Mystery</span></h1>
                <h2>Select Your Character</h2>
                <div className="character-select">
                    {constants.suspects.map(s => (
                        <button key={s} onClick={() => startGame(s)}>{s}</button>
                    ))}
                </div>
            </div>
        );
    }

    return (
        <div className="app-container">
            <div className="main-content">
                <div className="left-panel">
                    <div className="notebook-container">
                        <Notebook
                            gameState={gameState}
                            constants={constants}
                            humanCharacter={humanCharacter}
                        />
                    </div>
                    <div className="logs-container">
                        <h3>Game Log</h3>
                        <h4>Because I'm a backend developer</h4>
                        <div className="logs">
                            {gameState.logs.map((log, i) => (
                                <div key={i} className="log-entry">{log}</div>
                            ))}
                            <div ref={logsEndRef} />
                        </div>
                    </div>
                </div>

                <div className="center-panel">
                    <div className="board-container">
                        <button className="info-button" onClick={() => setShowRules(true)} title="Game Rules & AI Info">
                            i
                        </button>
                        {showRules && <RulesModal onClose={() => setShowRules(false)} />}
                        <Board gameState={gameState} onMove={refreshState} />
                    </div>
                    <div className="hand-section">
                        <Hand gameState={gameState} humanCharacter={humanCharacter} />
                    </div>
                </div>

                <div className="right-panel">
                    <div className="players-list-container">
                        <PlayersList gameState={gameState} />
                    </div>
                    <div className="controls-container">
                        <GameControls
                            gameState={gameState}
                            onAction={refreshState}
                            constants={constants}
                        />
                    </div>
                </div>
            </div>

            <VictoryModal gameState={gameState} />
        </div>
    );

}

export default App;
