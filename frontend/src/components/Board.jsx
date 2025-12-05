import React from 'react';
import { api } from '../api';
import './Board.css';
import { useState } from 'react';

const ROOM_LAYOUT = [
    ['Study', 'Hall', 'Billiard Room'],
    ['Library', 'Lounge', 'Dining Room'],
    ['Conservatory', 'Ballroom', 'Kitchen']
];

function Board({ gameState, onMove }) {
    if (!gameState) return null;

    const currentPlayer = gameState.players[gameState.current_player_index];
    const isHumanTurn = currentPlayer.is_human;
    // Only show available moves if dice have been rolled (and there are moves)
    const availableMoves = (gameState.dice_rolled && gameState.available_moves) ? gameState.available_moves : [];

    const handleRoomClick = async (roomName) => {
        if (isHumanTurn && availableMoves.includes(roomName)) {
            try {
                await api.move(roomName);
                onMove();
            } catch (err) {
                console.error("Move failed", err);
            }
        }
    };

    return (
        <div className="board">
            {ROOM_LAYOUT.map((row, rIndex) => (
                <div key={rIndex} className="board-row">
                    {row.map((roomName, cIndex) => {
                        const isAvailable = isHumanTurn && availableMoves.includes(roomName);
                        const playersInRoom = gameState.players.filter(p => p.position === roomName);

                        return (
                            <div
                                key={roomName}
                                className={`room ${isAvailable ? 'available' : ''}`}
                                onClick={() => handleRoomClick(roomName)}
                                style={{
                                    backgroundImage: `url("/images/rooms/${roomName}.png")`,
                                    backgroundSize: 'cover',
                                    backgroundPosition: 'center'
                                }}
                            >

                                <div className="players-container">
                                    {playersInRoom.map(p => (
                                        <div key={p.name} className={`player-token ${p.character_name.replace('.', '').replace(' ', '-').toLowerCase()}`} title={p.character_name}>
                                            {p.character_name.split(' ')[1][0]}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        );
                    })}
                </div>
            ))}
        </div>
    );
}

export default Board;
