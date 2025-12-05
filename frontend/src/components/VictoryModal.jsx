import React from 'react';
import './VictoryModal.css';

function VictoryModal({ gameState, onRestart }) {
    if (!gameState || gameState.phase !== 'game_over') return null;

    const winner = gameState.winner;
    const isHumanWinner = gameState.players.find(p => p.name === winner && p.is_human);

    return (
        <div className="victory-modal-overlay">
            <div className={`victory-modal ${isHumanWinner ? 'human-win' : 'ai-win'}`}>
                <div className="victory-content">
                    <h1>CASE CLOSED</h1>

                    <div className="winner-announcement">
                        <h2>Winner</h2>
                        <div className="winner-name">{winner}</div>
                    </div>

                    <div className="result-message">
                        {isHumanWinner ?
                            "Congratulations, Detective! You have solved the mystery!" :
                            "Better luck next time. The culprit has been identified by another detective."}
                    </div>

                    <button className="restart-button" onClick={() => window.location.reload()}>
                        Play Again
                    </button>
                </div>
            </div>
        </div>
    );
}

export default VictoryModal;
