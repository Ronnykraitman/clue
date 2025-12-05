import React from 'react';

function Notebook({ gameState, constants, humanCharacter }) {
    if (!gameState || !humanCharacter) return null;

    const humanPlayer = gameState.players.find(p => p.character_name === humanCharacter);
    const notebook = humanPlayer ? humanPlayer.notebook : {};
    const hand = humanPlayer ? humanPlayer.hand.map(c => c.name) : [];
    const seenCards = humanPlayer ? (humanPlayer.seen_cards || []) : [];

    const getStatus = (item) => {
        if (hand.includes(item)) return "HAND";
        if (seenCards.includes(item)) return "SEEN";
        return notebook[item] || "";
    };

    const getStatusClass = (status) => {
        if (status === "HAND") return "status-hand";
        if (status === "SEEN") return "status-seen";
        return "status-user";
    };

    return (
        <div className="notebook">
            <h3>Detective Notebook</h3>
            <div className="notebook-columns">
                <div className="column">
                    <h4>Suspects</h4>
                    {constants.suspects.map(s => {
                        const status = getStatus(s);
                        return (
                            <div key={s} className="notebook-item">
                                <span>{s}</span>
                                <span className={`status ${getStatusClass(status)}`}>{status}</span>
                            </div>
                        );
                    })}
                </div>
                <div className="column">
                    <h4>Weapons</h4>
                    {constants.weapons.map(w => {
                        const status = getStatus(w);
                        return (
                            <div key={w} className="notebook-item">
                                <span>{w}</span>
                                <span className={`status ${getStatusClass(status)}`}>{status}</span>
                            </div>
                        );
                    })}
                </div>
                <div className="column">
                    <h4>Rooms</h4>
                    {constants.rooms.map(r => {
                        const status = getStatus(r);
                        return (
                            <div key={r} className="notebook-item">
                                <span>{r}</span>
                                <span className={`status ${getStatusClass(status)}`}>{status}</span>
                            </div>
                        );
                    })}
                </div>
            </div>


            {
                humanPlayer && humanPlayer.undisproved_suspicions && humanPlayer.undisproved_suspicions.length > 0 && (
                    <div className="undisproved-section">
                        <h4>Undisproved Suspicions (Potential Solutions)</h4>
                        <ul>
                            {humanPlayer.undisproved_suspicions.map((item, idx) => (
                                <li key={idx}>
                                    <strong>{item.suspect}</strong> with <strong>{item.weapon}</strong> in <strong>{item.room}</strong>
                                </li>
                            ))}
                        </ul>
                    </div>
                )
            }
        </div>
    );
}

export default Notebook;
