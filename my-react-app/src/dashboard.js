import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';

// Layout Component (no changes needed here)
const Layout = ({ children, setIsAuthenticated }) => {
  const [isSidebarVisible, setIsSidebarVisible] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const toggleSidebar = () => {
    setIsSidebarVisible(!isSidebarVisible);
  };

  const goHome = () => {
    navigate('/balance');
  };

  const handleSignOut = () => {
    if (setIsAuthenticated) {
      setIsAuthenticated(false);
    }
    navigate('/');
  };

  const handleTutorialClick = () => {
    window.location.href = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"; //MAGGIE SAYS PLEASE FOR THE LOVE OF GOD REMEMBER TO CHANGE THIS
  };

  return (
    <div className="w-full flex min-h-screen">
      {/* Sidebar */}
      <div className={`w-64 bg-gray-800 text-white fixed top-0 left-0 bottom-0 p-6 transition-transform duration-300 ease-in-out ${isSidebarVisible ? 'transform-none' : '-translate-x-full'}`}>
        <h2 className="text-xl font-bold mb-4">Moves</h2>
        <button onClick={goHome} className="block px-3 py-2 mb-4 text-lg font-medium text-white bg-gray-700 rounded-md hover:bg-gray-600">
          Home
        </button>
        {location.pathname === '/balance' && (
          <button onClick={handleSignOut} className="block px-3 py-2 mt-4 text-lg font-medium text-white bg-red-600 rounded-md hover:bg-red-500">
            Sign Out
          </button>
        )}
        {/* Tutorial Button */}
        <button onClick={handleTutorialClick} className="block px-3 py-2 mt-4 text-lg font-medium text-white bg-green-600 rounded-md hover:bg-green-500">
          Tutorial
        </button>
      </div>

      <div className="flex-1">
        {/* Navbar */}
        <nav className="w-full bg-gray-800 p-4">
          <div className="flex items-center">
            <div className="shrink-0"></div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <Link to="/" className="rounded-md bg-gray-900 px-3 py-2 text-sm font-medium text-white" aria-current="page">
                  Dashboard
                </Link>
                <Link to="/calendar" className="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white">
                  Calendar
                </Link>
                <Link to="/logs" className="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white">
                  Reports
                </Link>
                <button onClick={toggleSidebar} className="absolute top-4 right-2 px-4 py-2 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600">
                  {isSidebarVisible ? 'Hide Sidebar' : 'Show Sidebar'}
                </button>
              </div>
            </div>
          </div>
        </nav>

        {/* Content */}
        <div>{children}</div>
      </div>
    </div>
  );
};

export default Layout;
