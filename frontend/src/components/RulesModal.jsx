import React from 'react';
import './RulesModal.css';

function RulesModal({ onClose }) {
    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal rules-modal" onClick={e => e.stopPropagation()}>
                <div className="rules-header">
                    <h2>Confidential Case Files</h2>
                    <div className="stamp">TOP SECRET</div>
                </div>

                <div className="rules-content">
                    <section className="objective-section">
                        <h3>The Objective</h3>
                        <p>
                            A murder has been committed! You must deduce the <strong>Who</strong>, <strong>Where</strong>, and <strong>With What</strong>.
                            Be the first to solve the mystery to win.
                        </p>
                    </section>

                    <section className="flow-section">
                        <h3>Investigation Flow</h3>
                        <div className="flow-timeline">
                            <div className="flow-step">
                                <div className="step-icon">🎲</div>
                                <div className="step-label">Roll & Move</div>
                            </div>
                            <div className="flow-line"></div>
                            <div className="flow-step">
                                <div className="step-icon">🔍</div>
                                <div className="step-label">Suspect</div>
                                <div className="step-desc">Suggest a solution in a room</div>
                            </div>
                            <div className="flow-line"></div>
                            <div className="flow-step">
                                <div className="step-icon">✋</div>
                                <div className="step-label">Disprove</div>
                                <div className="step-desc">Others show cards to prove you wrong</div>
                            </div>
                            <div className="flow-line"></div>
                            <div className="flow-step">
                                <div className="step-icon">⚖️</div>
                                <div className="step-label">Accuse</div>
                                <div className="step-desc">Final guess. Wrong? You lose!</div>
                            </div>
                        </div>
                    </section>

                    <section className="ai-section">
                        <h3>Intelligence Report (AI)</h3>
                        <div className="ai-grid">
                            <div className="ai-card">
                                <h4>🧠 Photographic Memory</h4>
                                <p>The AI never forgets a card it has seen. If you show it a card, it's marked in their notebook forever.</p>
                            </div>
                            <div className="ai-card">
                                <h4>🕵️ Deductive Logic</h4>
                                <p>The AI uses elimination. If it knows 5 suspects are innocent, it <em>knows</em> the 6th is guilty.</p>
                            </div>
                        </div>
                    </section>
                </div>

                <div className="modal-actions">
                    <button onClick={onClose}>Close File</button>
                </div>
            </div>
        </div>
    );
}

export default RulesModal;
