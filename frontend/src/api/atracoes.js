import axios from "axios";

const url = "http://localhost:8000";

export const get_atracoes = async (cidades) => {
    try {
        const response = await axios.get(`${url}/atracoes_monumentos`, {
            params: {
                cidades: Array.isArray(cidades) ? cidades : [cidades]
            }
        });
        return response.data;
    } catch (error) {
        console.error("Erro ao buscar atrações:", error);
        throw error;
    }
}