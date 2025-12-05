import React from 'react';
import './PlayersList.css';

function PlayersList({ gameState }) {
    if (!gameState) return null;

    return (
        <div className="players-list">
            <h3>Players</h3>
            <div className="players-grid">
                {gameState.players.map((player, index) => {
                    const isCurrentTurn = index === gameState.current_player_index;
                    return (
                        <div
                            key={player.name}
                            className={`player-card ${isCurrentTurn ? 'active-turn' : ''} ${player.is_eliminated ? 'eliminated' : ''}`}
                        >
                            <div className={`player-avatar ${player.character_name.replace('.', '').replace(' ', '-').toLowerCase()}`}>
                                {player.character_name.split(' ')[1][0]}
                            </div>
                            <div className="player-info">
                                <div className="player-name">
                                    {player.name} {player.is_human && player.name !== 'You' ? '(You)' : ''}
                                </div>
                                <div className="character-name">{player.character_name}</div>
                                {isCurrentTurn && <div className="turn-indicator">Current Turn</div>}
                                {player.is_eliminated && <div className="eliminated-badge">Eliminated</div>}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}

export default PlayersList;
