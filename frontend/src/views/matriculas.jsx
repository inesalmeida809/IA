import { useState } from "react";
import { useNavigate } from "react-router";
import { loginWithImage } from "../api/login";

const Login = () => {
  const navigate = useNavigate();
  const [imagem, setImagem] = useState(null);
  const [preview, setPreview] = useState(null);
  const [matricula, setMatricula] = useState("");
  const [mensagem, setMensagem] = useState("");
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");

  const handleImagemChange = (e) => {
    const file = e.target.files?.[0];

    if (!file) return;

    setImagem(file);
    setPreview(URL.createObjectURL(file));
    setMatricula("");
    setMensagem("");
    setErro("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!imagem) {
      setErro("Selecione uma imagem primeiro.");
      return;
    }

    try {
      setLoading(true);
      setErro("");
      setMatricula("");
      setMensagem("");

      const data = await loginWithImage(imagem);
      const matriculaLida = typeof data.matricula === 'string' ? data.matricula.trim() : "";

      if (!matriculaLida) {
        setErro(data.mensagem || "Matrícula não encontrada. Tente outra imagem.");
        setMensagem("");
        setMatricula("");
        return;
      }

      setMatricula(matriculaLida);
      setMensagem(data.mensagem || "Pedido concluído com sucesso.");
      sessionStorage.setItem("matricula", matriculaLida);
      navigate("/search", { state: { matricula: matriculaLida } });
    } catch (error) {
      console.error(error);
      setErro("Não foi possível ler a matrícula.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-2xl bg-white rounded-2xl shadow-lg overflow-hidden">
        <div className="bg-primary text-white px-6 py-5">
          <h1 className="text-2xl md:text-3xl font-bold">Leitor de matrículas</h1>
          <p className="text-sm md:text-base mt-1 opacity-90">
            Envie uma foto do veículo para extrair a matrícula automaticamente.
          </p>
        </div>

        <div className="p-6 md:p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">
                Escolher imagem
              </label>

              <input
                type="file"
                accept="image/*"
                onChange={handleImagemChange}
                className="block w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-700 file:mr-4 file:rounded-lg file:border-0 file:bg-primary file:px-4 file:py-2 file:text-white hover:file:bg-primary-dark"
              />
            </div>

            {preview && (
              <div className="border border-slate-200 rounded-2xl p-4 bg-slate-50">
                <p className="text-sm font-medium text-slate-700 mb-3">Pré-visualização</p>
                <img
                  src={preview}
                  alt="Preview da matrícula"
                  className="w-full max-h-[400px] object-contain rounded-xl"
                />
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full md:w-auto bg-primary hover:bg-primary-dark text-white font-semibold px-6 py-3 rounded-xl transition disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {loading ? "A processar..." : "Ler matrícula"}
            </button>
          </form>

          {erro && (
            <div className="mt-6 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-red-700">
              {erro}
            </div>
          )}

          {(matricula || mensagem) && !erro && (
            <div className="mt-6 rounded-2xl border border-green-200 bg-green-50 p-5">
              <p className="text-sm text-slate-600 mb-2">Resultado</p>
              <p className="text-2xl font-bold text-green-700 tracking-widest">
                {matricula || "Sem matrícula detetada"}
              </p>
              {mensagem && (
                <p className="text-sm text-slate-600 mt-2">{mensagem}</p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Login;