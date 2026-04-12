import React, { useEffect } from 'react';
import { useState } from 'react';
import { a_star, custo_uniforme, profundidade_limitada, procura_sofrega, get_cities } from '../api/methods';

function Search() {
    const [cities, setCities] = useState([]);
    const fetch_cities = async () => {
        try {
            const cities = await get_cities();
            setCities(cities);
            console.log("Cidades carregadas:", cities);
            return cities;
        } catch (error) {
            console.error("Erro ao procurar cidades:", error);
        }
    }

    const fetch_path = async (method, origem, destino) => {
        try {
            let response;
            if (method == "a_star") {
                response = await a_star(origem, destino); 
            } else if (method == "custo_uniforme") {
                response = await custo_uniforme(origem, destino); 
            } else if (method == "profundidade_limitada") {
                response = await profundidade_limitada(origem, destino); 
            } else if (method == "procura_sofrega") {
                response = await procura_sofrega(origem, destino); 
            } else {
                throw new Error("Método de pesquisa desconhecido");
            }
            console.log("Resposta do servidor:", response);
        } catch (error) {
            console.error("Erro ao encontrar caminho:", error);
        }
    }

    useEffect(() => {
        fetch_cities();
    }, []);

    return (
        <div>
            <form onSubmit={(e) => {
                e.preventDefault();
                const formData = new FormData(e.target);
                const origem = formData.get("origem");
                const destino = formData.get("destino");
                const method = formData.get("method");
                fetch_path(method, origem, destino);
            }}>
                <div>
                    <label htmlFor="">Origem</label>
                    <select name="origem" id="origem" defaultValue="">
                        <option value="" disabled>Selecione a origem</option>
                        {cities.map((city) => (
                            <option key={city} value={city}>{city}</option>
                        ))}
                    </select>
                </div>
                <div>
                    <label htmlFor="destino">Destino</label>
                    <select name="destino" id="destino" defaultValue="">
                        <option value="" disabled>Selecione o destino</option>
                        {cities.map((city) => (
                            <option key={city} value={city}>{city}</option>
                        ))}
                    </select>
                </div>
                <div>
                    <label htmlFor="method">Método de pesquisa</label>
                    <select name="method" id="method" defaultValue="">
                        <option value="" disabled>Selecione o método</option>
                        <option value="a_star">A*</option>
                        <option value="custo_uniforme">Custo Uniforme</option>
                        <option value="profundidade_limitada">Profundidade Limitada</option>
                        <option value="procura_sofrega">Procura Sofrega</option>
                    </select>
                </div>
                <button type="submit">Pesquisar Caminho</button>
            </form>
            <div>MAPA</div>
        </div>
    );
}

export default Search;