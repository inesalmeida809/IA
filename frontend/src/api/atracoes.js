import axios from "axios";

const url = "http://localhost:8000";

export const get_atracoes = async (cidades) => {
    try {
        const cidadesArray = Array.isArray(cidades) ? cidades : [cidades];
        const searchParams = new URLSearchParams();
        cidadesArray.forEach((cidade) => searchParams.append('cidades', cidade));

        const response = await axios.get(`${url}/atracoes_monumentos?${searchParams.toString()}`);
        return response.data;
    } catch (error) {
        console.error("Erro ao buscar atrações:", error);
        throw error;
    }
}