import axios from 'axios';

const API_URL = import.meta.env.PROD ? '/clue/api' : 'http://localhost:8001';

export const api = {
    startGame: (humanCharacter) => axios.post(`${API_URL}/game/start`, { human_character: humanCharacter }),
    getState: () => axios.get(`${API_URL}/game/state`),
    rollDice: () => axios.post(`${API_URL}/game/roll`),
    move: (destination) => axios.post(`${API_URL}/game/move`, { destination_room: destination }),
    suspect: (suspect, weapon, room) => axios.post(`${API_URL}/game/suspect`, { suspect, weapon, room }),
    accuse: (suspect, weapon, room) => axios.post(`${API_URL}/game/accuse`, { suspect, weapon, room }),
    passTurn: () => axios.post(`${API_URL}/game/pass`),
    playAiTurn: () => axios.post(`${API_URL}/game/ai-turn`),
    getConstants: () => axios.get(`${API_URL}/game/constants`),
};
