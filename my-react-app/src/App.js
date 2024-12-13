import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css'; 
import ReportPage from './logs';
import CommentPage from './comments';
import Layout from './dashboard';
import UploadManifestPage from './UploadManifestPage';

import { useNavigate } from 'react-router-dom';

function BalancePage() {
  const navigate = useNavigate(); 

  const handleBalanceClick = () => {
    navigate('/upload-manifest');
  };

  return (
    <div className="app">
      <div className="flex items-center justify-center min-h-screen">
        <div>
          <button
            className="w-full px-32 py-2 mb-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 text-center"
            onClick={handleBalanceClick}  
          >
            Load/Unload
          </button>
        </div>

        <div
          className="w-full px-32 py-2 mb-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 text-center"
          onClick={handleBalanceClick} 
        >
          <h2>Balance</h2>
        </div>
      </div>
    </div>
  );
}

// Define the SignIn component
function SignIn({ setIsAuthenticated, setUsername }) {
  const [username, setLocalUsername] = useState('');

  const handleSignIn = (e) => {
    e.preventDefault();
    if (username.trim() !== '') {
      setUsername(username);  // Set username in App component
      setIsAuthenticated(true); // If there is a username then accept
    } else {
      alert('Please enter a username!');
    }
  };

  return (
    <div className="sign-in-container">
      <h1 className="text-2xl font-bold text-black-900 mb-10">Welcome to EZCargo</h1>
      <form onSubmit={handleSignIn}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setLocalUsername(e.target.value)}
          className="input-field"
        />
        <button type="submit" className="w-full px-32 py-2 mb-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
          Sign In
        </button>
      </form>
    </div>
  );
}

// Export the App component
function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState(''); // Store the username so we can display it

  return (
    <Router>
      <div className="app-container">
        <Routes>
          {/* SignIn route */}
          <Route
            path="/"
            element={
              isAuthenticated ? <Navigate to="/balance" replace /> : <SignIn setIsAuthenticated={setIsAuthenticated} setUsername={setUsername} />
            }
          />
          
          {/* Protected Routes */}
          <Route path="/balance" element={isAuthenticated ? <Layout setIsAuthenticated={setIsAuthenticated}><BalancePage /></Layout> : <Navigate to="/" replace />} />
          <Route path="/upload-manifest" element={isAuthenticated ? <UploadManifestPage /> : <Navigate to="/" replace />} />
          <Route path="/comment" element={isAuthenticated ? <Layout setIsAuthenticated={setIsAuthenticated}><CommentPage username={username} /></Layout> : <Navigate to="/" replace />}/>
          <Route path="/logs" element={isAuthenticated ? <ReportPage /> : <Navigate to="/" replace />} />
          
        </Routes>
      </div>
    </Router>
  );
}

export default App;
