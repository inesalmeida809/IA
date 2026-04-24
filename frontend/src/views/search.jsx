import React, { useEffect, useState, useMemo } from "react";
import { useLocation } from "react-router-dom";
import {
  a_star,
  custo_uniforme,
  profundidade_limitada,
  procura_sofrega,
  get_cities,
} from "../api/methods";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { get_atracoes } from "../api/atracoes";

function Search() {
  const [cities, setCities] = useState([]);
  const [error, setError] = useState("");
  const [matriculaLida, setMatriculaLida] = useState("");
  const [pathResult, setPathResult] = useState(null);
  const [loadingPath, setLoadingPath] = useState(false);
  const [loadingAtracoes, setLoadingAtracoes] = useState(false);
  const [atracoes, setAtracoes] = useState(null);
  const [selectedMethod, setSelectedMethod] = useState("");
  const [profundidadeLimite, setProfundidadeLimite] = useState("");
  const location = useLocation();

  const fetch_cities = async () => {
    try {
      const cities = await get_cities();
      setCities(cities);
      console.log("Cidades carregadas:", cities);
      return cities;
    } catch (error) {
      console.error("Erro ao procurar cidades:", error);
    }
  };

  const fetch_atracoes = async (cidades) => {
    try {
      setLoadingAtracoes(true);
      const response = await get_atracoes(cidades);
      console.log("Atrações recebidas:", response);
      setAtracoes(response);
    } catch (error) {
      console.error("Erro ao buscar atrações:", error);
      setAtracoes(null);
    } finally {
      setLoadingAtracoes(false);
    }
  };

  const fetch_path = async (method, origem, destino, limite = null) => {
    try {
      setLoadingPath(true);
      let response;

      if (method == "a_star") {
        response = await a_star(origem, destino);
      } else if (method == "custo_uniforme") {
        response = await custo_uniforme(origem, destino);
      } else if (method == "profundidade_limitada") {
        response = await profundidade_limitada(origem, destino, limite || null);
      } else if (method == "procura_sofrega") {
        response = await procura_sofrega(origem, destino);
      } else {
        throw new Error("Método de pesquisa desconhecido");
      }

      console.log("Resposta do servidor:", response);
      setPathResult(response);
      return response;
    } catch (error) {
      console.error("Erro ao encontrar caminho:", error);
      setPathResult(null);
      return null;
    } finally {
      setLoadingPath(false);
    }
  };

  useEffect(() => {
    const matricula =
      location.state?.matricula || sessionStorage.getItem("matricula") || "";

    setMatriculaLida(matricula);
    console.log("Matrícula recebida:", matricula);

    fetch_cities();
  }, [location.state]);

  useEffect(() => {
    if (pathResult?.caminho) {
      fetch_atracoes(pathResult.caminho);
    }
  }, [pathResult]);

  const polylinePositions = useMemo(() => {
    if (!pathResult?.coordenadas) return [];

    return pathResult.coordenadas.map((coord) => [coord[0], coord[1]]);
  }, [pathResult]);

  const mapCenter = useMemo(() => {
    if (polylinePositions.length > 0) return polylinePositions[0];

    return [39.5, -8.0];
  }, [polylinePositions]);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {matriculaLida ? (
        <div className="mb-6 rounded-2xl border border-green-200 bg-green-50 p-4 text-sm text-green-700">
          Matrícula lida: <span className="font-semibold">{matriculaLida}</span>
        </div>
      ) : (
        <div className="mb-6 rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
          Faça login com uma matrícula para ver o valor nesta página.
        </div>
      )}
      <div className="overflow-hidden rounded-3xl border border-orange-100 bg-white shadow-xl shadow-orange-100/40">
        <form
          onSubmit={async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const origem = formData.get("origem");
            const destino = formData.get("destino");
            const method = formData.get("method");
            if (!origem || !destino || !method) {
              setError("Todos os campos são obrigatórios.");
              return;
            } else {
              setError("");
              const limite =
                method === "profundidade_limitada"
                  ? profundidadeLimite || null
                  : null;
              const response = await fetch_path(
                method,
                origem,
                destino,
                limite,
              );
              if (response) {
                try {
                  /* await save_history({
                    matricula: matriculaLida,
                    pesquisa: {
                      origem,
                      destino,
                      metodo: method,
                      limite,
                      caminho: pathResult?.caminho,
                      custo: pathResult?.custo,
                      coordenadas: pathResult?.coordenadas,
                    },
                  }); */
                } catch (error) {
                  console.error("Erro ao enviar histórico de pesquisa:", error);
                }
              }
            }
          }}
          className="space-y-5 p-6"
        >
          <div>
            <label
              htmlFor="origem"
              className="mb-2 block text-sm font-semibold text-gray-700"
            >
              Origem
            </label>
            <select
              name="origem"
              id="origem"
              defaultValue=""
              className="w-full rounded-2xl border border-orange-200 bg-orange-50 px-4 py-3 text-sm text-gray-800 outline-none transition duration-200 focus:border-orange-500 focus:bg-white focus:ring-4 focus:ring-orange-100"
            >
              <option value="" disabled>
                Selecione a origem
              </option>
              {cities.map((city) => (
                <option key={city} value={city}>
                  {city}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label
              htmlFor="destino"
              className="mb-2 block text-sm font-semibold text-gray-700"
            >
              Destino
            </label>
            <select
              name="destino"
              id="destino"
              defaultValue=""
              className="w-full rounded-2xl border border-orange-200 bg-orange-50 px-4 py-3 text-sm text-gray-800 outline-none transition duration-200 focus:border-orange-500 focus:bg-white focus:ring-4 focus:ring-orange-100"
            >
              <option value="" disabled>
                Selecione o destino
              </option>
              {cities.map((city) => (
                <option key={city} value={city}>
                  {city}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label
              htmlFor="method"
              className="mb-2 block text-sm font-semibold text-gray-700"
            >
              Método de pesquisa
            </label>
            <select
              name="method"
              id="method"
              defaultValue=""
              onChange={(e) => {
                setSelectedMethod(e.target.value);
                setProfundidadeLimite("");
              }}
              className="w-full rounded-2xl border border-orange-200 bg-orange-50 px-4 py-3 text-sm text-gray-800 outline-none transition duration-200 focus:border-orange-500 focus:bg-white focus:ring-4 focus:ring-orange-100"
            >
              <option value="" disabled>
                Selecione o método
              </option>
              <option value="a_star">A*</option>
              <option value="custo_uniforme">Custo Uniforme</option>
              <option value="profundidade_limitada">
                Profundidade Limitada
              </option>
              <option value="procura_sofrega">Procura Sofrega</option>
            </select>
          </div>

          {selectedMethod === "profundidade_limitada" && (
            <div>
              <label
                htmlFor="profundidade"
                className="mb-2 flex items-center gap-2 text-sm font-semibold text-gray-700"
              >
                Limite de Profundidade
                <span className="text-xs font-normal text-gray-500">
                  (Opcional - padrão: 10)
                </span>
              </label>
              <input
                type="number"
                name="profundidade"
                id="profundidade"
                min="1"
                defaultValue=""
                placeholder="Deixe em branco para usar o valor padrão (10)"
                value={profundidadeLimite}
                onChange={(e) =>
                  setProfundidadeLimite(
                    e.target.value ? parseInt(e.target.value) : "",
                  )
                }
                className="w-full rounded-2xl border border-orange-200 bg-orange-50 px-4 py-3 text-sm text-gray-800 outline-none transition duration-200 focus:border-orange-500 focus:bg-white focus:ring-4 focus:ring-orange-100"
              />
            </div>
          )}
          {error && (
            <div className="mb-4 flex items-start gap-3 rounded-2xl border border-orange-200 bg-orange-50 px-4 py-3 text-sm text-orange-800">
              <span className="text-lg">⚠️</span>
              <p>{error}</p>
            </div>
          )}
          <button
            type="submit"
            disabled={loadingPath}
            className="inline-flex w-full items-center justify-center rounded-2xl bg-orange-500 px-5 py-3.5 text-sm font-semibold text-white shadow-lg shadow-orange-200 transition duration-200 hover:-translate-y-0.5 hover:bg-orange-600 hover:shadow-orange-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loadingPath ? "A pesquisar..." : "Pesquisar Caminho"}
          </button>
        </form>
      </div>

      {pathResult && (
        <div className="mt-6 rounded-2xl border border-green-200 bg-green-50 p-4">
          <h3 className="text-lg font-semibold text-green-800 mb-2">
            Resultado da Pesquisa
          </h3>
          <div className="text-sm text-green-700">
            <strong>Caminho:</strong>{" "}
            {pathResult.caminho?.join(" → ") || "Nenhum caminho encontrado"}
            {pathResult.custo && (
              <>
                <br />
                <strong>Custo:</strong> {pathResult.custo}
              </>
            )}
            {pathResult.distancia && (
              <>
                <br />
                <strong>Distância:</strong> {pathResult.distancia}
              </>
            )}
          </div>
        </div>
      )}

      <div className="mt-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          Mapa do Caminho e Atrações
        </h3>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Mapa - ocupa 2 colunas em desktop, 1 em mobile */}
          <div className="lg:col-span-2 rounded-2xl overflow-hidden border border-gray-200 shadow-lg">
            <MapContainer
              center={mapCenter}
              zoom={7}
              scrollWheelZoom={true}
              style={{ height: "500px", width: "100%" }}
            >
              <TileLayer
                attribution="&copy; OpenStreetMap contributors"
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />

              {pathResult?.caminho &&
                pathResult?.coordenadas &&
                pathResult.caminho.map((cityName, index) => {
                  const position = pathResult.coordenadas[index];
                  if (!position) return null;

                  return (
                    <Marker
                      key={`${cityName}-${index}`}
                      position={[position[0], position[1]]}
                    >
                      <Popup>
                        <strong>{cityName}</strong>
                        {index === 0 && " (Origem)"}
                        {index === pathResult.caminho.length - 1 &&
                          " (Destino)"}
                      </Popup>
                    </Marker>
                  );
                })}

              {polylinePositions.length > 1 && (
                <Polyline
                  positions={polylinePositions}
                  color="blue"
                  weight={4}
                  opacity={0.7}
                />
              )}
            </MapContainer>
          </div>

          {/* Painel de Atrações */}
          <div className="rounded-2xl border border-orange-100 bg-orange-50 shadow-lg overflow-hidden">
            <div className="p-4 bg-orange-500 text-white">
              <h3 className="text-lg font-bold">Atrações e Monumentos</h3>
            </div>

            <div className="p-4 overflow-y-auto" style={{ height: "500px" }}>
              {loadingAtracoes ? (
                <div className="flex items-center justify-center h-full">
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500 mx-auto mb-2"></div>
                    <p className="text-sm text-orange-600">
                      A carregar atrações...
                    </p>
                  </div>
                </div>
              ) : atracoes && atracoes.length > 0 ? (
                <div className="space-y-5">
                  {atracoes.map((item) => (
                    <div
                      key={item.distrito}
                      className="bg-white rounded-xl p-4 shadow-sm border-l-4 border-orange-400 hover:shadow-md transition-shadow"
                    >
                      <h4 className="font-semibold text-orange-700 mb-3 text-sm uppercase tracking-wide">
                        {item.distrito}
                      </h4>
                      <div className="space-y-3">
                        {item.atracoes?.map((atracao, index) => (
                          <div
                            key={`${item.distrito}-${index}`}
                            className="rounded-2xl bg-orange-50 p-3"
                          >
                            <p className="font-semibold text-gray-900">
                              {atracao.nome}
                            </p>
                            <p className="text-sm text-gray-600 leading-relaxed mt-1">
                              {atracao.descricao}
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="flex items-center justify-center h-full text-center text-gray-500">
                  <p className="text-sm">
                    Pesquise um caminho para ver as atrações das cidades
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Search;
