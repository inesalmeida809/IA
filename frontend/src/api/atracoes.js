const url = "http://localhost:8000/";

export const get_atracoes = async (cidades, onData) => {
    try {
        const cidadesArray = Array.isArray(cidades) ? cidades : [cidades];
        const search = new URLSearchParams();

        cidadesArray.forEach((cidade) => {
            search.append("cidades", cidade);
        });

        const response = await fetch(`${url}atracoes_monumentos?${search.toString()}`);
        if (!response.ok) {
            throw new Error(`Erro na resposta: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let buffer = "";

        while (true) {
            const { done, value } = await reader.read();
            
            if (done) break; 

            buffer += decoder.decode(value, { stream: true });
            
            const linhas = buffer.split('\n');
            
            buffer = linhas.pop();

            for (let linha of linhas) {
                if (linha.trim() !== '') {
                    try {
                        const dadosTratados = JSON.parse(linha);
                        onData(dadosTratados);
                    } catch (err) {
                        console.error("Erro ao fazer parse do JSON:", err, linha);
                    }
                }
            }
        }

        if (buffer.trim() !== '') {
            try {
                onData(JSON.parse(buffer));
            } catch (err) {
                console.error("Erro final no parse:", err, buffer);
            }
        }
    } catch (error) {
        console.error("Erro ao buscar atrações:", error);
        throw error;
    }
}