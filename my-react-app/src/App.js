import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import './App.css'; 
import ReportPage from './logs';
import CommentPage from './comments';
import axios from "axios";
import Layout from './dashboard';
import { Outlet } from 'react-router-dom'; 



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
      <h1 className="text-2xl font-bold text-black-900 mb-10" >Welcome to EZCargo</h1>
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
        <div class="text-sm">
            <a href="google.com" class="font-semibold text-indigo-600 hover:text-indigo-500">Forgot password?</a>
        </div>
        </form>
    </div>
  );
}






function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <Router>
      <div className ="app-container"> 
      <Routes>
        <Route
          path="/"
          element={
            isAuthenticated ? <Navigate to="/comment" replace /> : <SignIn setIsAuthenticated={setIsAuthenticated} />
          }
        />
        <Route path="/comment" element={isAuthenticated ? <CommentPage /> : <Navigate to="/" replace />} />
        <Route path="/logs" element={isAuthenticated ? <ReportPage /> : <Navigate to="/" replace />} />
      </Routes>
      </div>
    </Router>
  );
}

export default App;
