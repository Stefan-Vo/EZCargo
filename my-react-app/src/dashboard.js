import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Layout = ({ children }) => {
  const [isSidebarVisible, setIsSidebarVisible] = useState(false);

  // Function to toggle the sidebar visibility
  const toggleSidebar = () => {
    setIsSidebarVisible(!isSidebarVisible);
  };

  return (
    <div className="w-full flex min-h-screen">
      {/* Sidebar */}
      {isSidebarVisible && (
        <div className="w-64 bg-gray-800 text-white fixed top-0 bottom-0 right-0 p-6">
          <h2 className="text-xl font-bold mb-4">Moves</h2>
        </div>
      )}
      
      <div className="">
        {/* Navbar */}
        <nav className="w-full bg-gray-800 p-4">
          <div className="flex items-center">
            <div className="shrink-0"></div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <Link
                  to="/"
                  className="rounded-md bg-gray-900 px-3 py-2 text-sm font-medium text-white"
                  aria-current="page"
                >
                  Dashboard
                </Link>
                <Link
                  to="/calendar"
                  className="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white"
                >
                  Calendar
                </Link>
                <Link
                  to="/logs"
                  className="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white"
                >
                  Reports
                </Link>
                <button
                  onClick={toggleSidebar}
                  className="absolute top-4 right-2 px-4 py-2 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600"
                >
                  {isSidebarVisible ? 'Hide Sidebar' : 'Show Sidebar'}
                </button>
              </div>
            </div>
          </div>
        </nav>

        {/* Content */}
        <div>
          {/* Render the children content */}
          {children}
        </div>
      </div>
    </div>
  );
};

export default Layout;