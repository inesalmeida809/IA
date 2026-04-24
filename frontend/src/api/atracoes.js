import axios from "axios";

const url = "http://localhost:8000/";

export const get_atracoes = async (cidades) => {
    try {
        const cidadesArray = Array.isArray(cidades) ? cidades : [cidades];
        const search = new URLSearchParams();

        cidadesArray.forEach((cidade) => {
            search.append("cidades", cidade);
        });

        const response = await axios.get(`${url}atracoes_monumentos?${search.toString()}`);
        return response.data;
    } catch (error) {
        console.error("Erro ao buscar atrações:", error);
        throw error;
    }
}