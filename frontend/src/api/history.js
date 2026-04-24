import axios from "axios";

const url = "http://localhost:8000/save-history";

export const save_plate = async (plate) => {
    try {
        const response = await axios.post(`${url}/plate`, { plate });
        return response.data;
    } catch (error) {
        throw error;
    }
}

export const save_history = async (historyData) => {
    try {
        const response = await axios.post(`${url}/history`, historyData);
        return response.data;
    } catch (error) {
        throw error;
    }
}