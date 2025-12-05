import React from 'react';
import './Hand.css';

function Hand({ gameState, humanCharacter }) {
    if (!gameState || !humanCharacter) return null;

    const humanPlayer = gameState.players.find(p => p.character_name === humanCharacter);
    if (!humanPlayer) return null;

    return (
        <div className="hand-container">
            <h3>Your Hand</h3>
            <div className="cards-list">
                {humanPlayer.hand.map((card, index) => (
                    <div key={index} className={`card ${card.type}`}>
                        <div className="card-image-container">
                            <img
                                src={card.type === 'room' ? `/images/rooms/${card.name}.png` : `/images/cards/${card.name}.png`}
                                alt={card.name}
                                className="card-image"
                                onError={(e) => {
                                    e.target.onerror = null;
                                    e.target.style.display = 'none';
                                    e.target.parentElement.classList.add('no-image');
                                }}
                            />
                        </div>
                        <div className="card-content">
                            <div className="card-name">{card.name}</div>
                            <div className="card-type">{card.type.toUpperCase()}</div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Hand;
