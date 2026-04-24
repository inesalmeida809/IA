import { Outlet, useNavigate } from 'react-router-dom';

const Base = () => {
  const navigate = useNavigate();
  const matricula = sessionStorage.getItem('matricula');

  const handleLogout = () => {
    sessionStorage.removeItem('matricula');
    navigate('/login', { replace: true });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex-shrink-0">
              <div className="flex items-center">
                <img
                  src="/src/assets/logo.png"
                  alt="Logo"
                  className="h-10 w-auto"
                />
              </div>
            </div>

            {matricula && (
              <button
                type="button"
                onClick={handleLogout}
                className="rounded-xl bg-red-500 px-4 py-2 text-sm font-semibold text-white transition hover:bg-red-600"
              >
                Logout
              </button>
            )}
          </div>
        </div>
      </header>

      <main className="flex-1">
        <Outlet />
      </main>
    </div>
  );
};

export default Base;