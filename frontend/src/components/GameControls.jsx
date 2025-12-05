import React, { useState } from 'react';
import { api } from '../api';

function GameControls({ gameState, onAction, constants }) {
    const [suspicion, setSuspicion] = useState({ suspect: '', weapon: '' });
    const [accusation, setAccusation] = useState({ suspect: '', weapon: '', room: '' });
    const [showSuspectModal, setShowSuspectModal] = useState(false);
    const [showAccuseModal, setShowAccuseModal] = useState(false);
    const [lastRoll, setLastRoll] = useState(null);
    const [suspicionResult, setSuspicionResult] = useState(null);

    if (!gameState) return null;

    const currentPlayer = gameState.players[gameState.current_player_index];
    const isHumanTurn = currentPlayer.is_human;
    const phase = gameState.phase;

    // Reset roll when player changes
    React.useEffect(() => {
        setLastRoll(null);
    }, [gameState.current_player_index]);

    const handleRoll = async () => {
        try {
            const res = await api.rollDice();
            setLastRoll(res.data.roll);
            onAction();
        } catch (err) {
            console.error(err);
        }
    };

    const handlePass = async () => {
        try {
            await api.passTurn();
            onAction();
        } catch (err) {
            console.error(err);
        }
    };

    const handleSuspect = async () => {
        try {
            const res = await api.suspect(suspicion.suspect, suspicion.weapon, currentPlayer.position);
            setSuspicionResult(res.data.result);
            setShowSuspectModal(false);
            // Do NOT call onAction() yet. Wait for user to acknowledge result.
        } catch (err) {
            console.error(err);
        }
    };

    const handleAccuse = async () => {
        try {
            await api.accuse(accusation.suspect, accusation.weapon, accusation.room);
            setShowAccuseModal(false);
            onAction();
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div className="controls">
            <h3>Current Turn: {currentPlayer.name} ({currentPlayer.character_name})</h3>

            {lastRoll && <div className="dice-report">You rolled a {lastRoll}!</div>}

            {isHumanTurn && (
                <div className="actions">
                    {phase === 'player_turn_move' && !gameState.dice_rolled && (
                        <div className="roll-section">
                            <button className="roll-button" onClick={handleRoll}>Roll Dice</button>
                        </div>
                    )}

                    {gameState.dice_rolled && phase === 'player_turn_move' && (
                        <div className="roll-section">
                            <p className="instruction">Select a glowing room to move.</p>
                        </div>
                    )}

                    {phase === 'player_turn_action' && (
                        <div className="turn-actions">
                            <div className="primary-actions">
                                <button onClick={() => { setShowSuspectModal(true); setShowAccuseModal(false); }}>Suspect</button>
                                <button onClick={() => { setShowAccuseModal(true); setShowSuspectModal(false); }}>Accuse</button>
                            </div>
                            <button className="pass-button" onClick={handlePass}>Pass Turn</button>
                        </div>
                    )}

                    {showSuspectModal && (
                        <div className="inline-form">
                            <h4>Make a Suspicion</h4>
                            <p>Room: {currentPlayer.position}</p>
                            <select onChange={e => setSuspicion({ ...suspicion, suspect: e.target.value })}>
                                <option value="">Select Suspect</option>
                                {constants.suspects.map(s => <option key={s} value={s}>{s}</option>)}
                            </select>
                            <select onChange={e => setSuspicion({ ...suspicion, weapon: e.target.value })}>
                                <option value="">Select Weapon</option>
                                {constants.weapons.map(w => <option key={w} value={w}>{w}</option>)}
                            </select>
                            <div className="form-actions">
                                <button onClick={handleSuspect}>Submit</button>
                                <button className="cancel-button" onClick={() => setShowSuspectModal(false)}>Cancel</button>
                            </div>
                        </div>
                    )}

                    {showAccuseModal && (
                        <div className="inline-form">
                            <h4>Make an Accusation</h4>
                            <p className="warning">WARNING: Wrong accusation eliminates you!</p>
                            <select onChange={e => setAccusation({ ...accusation, room: e.target.value })}>
                                <option value="">Select Room</option>
                                {constants.rooms.map(r => <option key={r} value={r}>{r}</option>)}
                            </select>
                            <select onChange={e => setAccusation({ ...accusation, suspect: e.target.value })}>
                                <option value="">Select Suspect</option>
                                {constants.suspects.map(s => <option key={s} value={s}>{s}</option>)}
                            </select>
                            <select onChange={e => setAccusation({ ...accusation, weapon: e.target.value })}>
                                <option value="">Select Weapon</option>
                                {constants.weapons.map(w => <option key={w} value={w}>{w}</option>)}
                            </select>
                            <div className="form-actions">
                                <button onClick={handleAccuse}>Accuse!</button>
                                <button className="cancel-button" onClick={() => setShowAccuseModal(false)}>Cancel</button>
                            </div>
                        </div>
                    )}
                </div>
            )}

            {suspicionResult && (
                <div className="modal-overlay">
                    <div className="modal result-modal">
                        <h4>Suspicion Result</h4>
                        {suspicionResult.has_card ? (
                            <p>
                                <strong>{suspicionResult.player}</strong> showed you:
                                <br />
                                <span className="revealed-card">{suspicionResult.card.name}</span> ({suspicionResult.card.type})
                            </p>
                        ) : (
                            <p>No one could disprove your suspicion!</p>
                        )}
                        <div className="modal-actions">
                            <button onClick={() => {
                                setSuspicionResult(null);
                                onAction(); // Proceed to next turn only after acknowledgement
                            }}>Acknowledge & End Turn</button>
                        </div>
                    </div>
                </div>
            )}


        </div>
    );
}

export default GameControls;
