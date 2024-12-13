import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css'; 
import ReportPage from './logs';
import CommentPage from './comments';
import axios from "axios";
import Layout from './dashboard';
import { Outlet } from 'react-router-dom';
import UploadManifestPage from './UploadManifestPage';

import { useNavigate } from 'react-router-dom';

// Define the BalancePage component
function BalancePage() {
  const navigate = useNavigate(); // Hook to navigate programmatically

  const handleBalanceClick = () => {
    navigate('/upload-manifest'); // Navigate to the upload page
  };

  return (
    <div className="balance-container">
      <h1 className="page-title">Load/Unload or Balance</h1>
      <div className="boxes-container">
        <div className="box load-unload-box">
          <h2>Load/Unload</h2>
        </div>
        <div
          className="box balance-box"
          onClick={handleBalanceClick} // Add the click event
        >
          <h2>Balance</h2>
        </div>
      </div>
    </div>
  );
}

// Define the SignIn component
function SignIn({ setIsAuthenticated }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSignIn = (e) => {
    e.preventDefault();
    if (username === 'test' && password === 'test') {
      setIsAuthenticated(true);
    } else {
      alert('Invalid credentials! Try "admin" / "password".');
    }
  };

  return (
    <div className="sign-in-container">
      <h1 className="text-2xl font-bold text-black-900 mb-10">Welcome to EZCargo</h1>
      <form onSubmit={handleSignIn} className="">
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="input-field"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="input-field"
        />
        <button type="submit" className="w-full px-32 py-2 mb-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
          Sign In
        </button>
        <button type="submit" className="w-full px-32 py-2 mb-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
          Register
        </button>
        <div className="text-sm">
          <a href="google.com" className="font-semibold text-indigo-600 hover:text-indigo-500">Forgot password?</a>
        </div>
      </form>
    </div>
  );
}

// Export the App component
function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <Router>
      <div className="app-container">
        <Routes>
          <Route
            path="/"
            element={
              isAuthenticated ? <Navigate to="/balance" replace /> : <SignIn setIsAuthenticated={setIsAuthenticated} />
            }
          />
          <Route path="/balance" element={isAuthenticated ? <BalancePage /> : <Navigate to="/" replace />} />
          <Route path="/upload-manifest" element={isAuthenticated ? <UploadManifestPage /> : <Navigate to="/" replace />} />
          <Route path="/comment" element={isAuthenticated ? <CommentPage /> : <Navigate to="/" replace />} />
          <Route path="/logs" element={isAuthenticated ? <ReportPage /> : <Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App; 
