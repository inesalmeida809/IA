import axios from "axios";

const url = "http://localhost:8000/";

export const get_cities = async () => {
    try {
        const response = await axios.get(`${url}cities`);
        console.log("Resposta do servidor:", response.data);
        return response.data.cidades;
    } catch (error) {
        throw error;
    }
}

export const a_star = async (partida, destino) => {
    try {
        const response = await axios.get(`${url}a-star`, {
            params: {
                partida,
                destino
            }
        });
        return response.data;
    } catch (error) {
        throw error;
    }
}

export const custo_uniforme = async (partida, destino) => {
    try {
        const response = await axios.get(`${url}custo-uniforme`, {
            params: {
                partida,
                destino
            }
        });
        return response.data;
    } catch (error) {
        throw error;
    }
}

export const profundidade_limitada = async (partida, destino) => {
    try {
        const response = await axios.get(`${url}profundidade-limitada`, {
            params: {
                partida,
                destino
            }
        });
        return response.data;
    } catch (error) {
        throw error;
    }
}

export const procura_sofrega = async (partida, destino) => {
    try {
        const response = await axios.get(`${url}procura-sofrega`, {
            params: {
                partida,
                destino
            }
        });
        return response.data;
    } catch (error) {
        throw error;
    }
}

