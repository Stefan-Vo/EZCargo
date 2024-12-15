import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import './App.css'; 
import ReportPage from './logs.js';
import CommentPage from './comments.js';
import axios from "axios";
import Layout from './dashboard';
import { Outlet } from 'react-router-dom'; 
import Calendar from './Calendar.js';
import FileUpload from './fileupload.js';
import OperationsPage from './operationspage.js';
import CommentLoad from './commentload.js';



function SignIn({ setIsAuthenticated, setUserName }) {
  const [userName, setUsername] = useState('');

  const handleSignIn = (e) => {
    e.preventDefault();
    if (userName.trim()) {  // Just check if username is not empty
      setIsAuthenticated(true);
      setUserName(userName);  // Save the username
    } else {
      alert('Please enter your name');
    }
  };

  return (
    <div className="">
      <div className="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-lg">
        <div>
          <h1 className="text-center text-3xl font-extrabold text-gray-900">
            Welcome to EZCargo
          </h1>
          <p className="mt-2 text-center text-sm text-gray-600">
            Please sign in to continue
          </p>
        </div>
        <form onSubmit={handleSignIn} className="mt-8 space-y-6">
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="username" className="sr-only">
                Username
              </label>
              <input
                id="username"
                type="text"
                placeholder="Enter your name"
                value={userName}
                onChange={(e) => setUsername(e.target.value)}
                className="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              />
            </div>
          </div>
  
          <div>
            <button
              type="submit"
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
            >
              <span className="absolute left-0 inset-y-0 flex items-center pl-3">
                {/* Optional: Add an icon here */}
              </span>
              Sign In
            </button>
          </div>
        </form>
  
        {/* Optional: Add additional links or information */}
        <div className="mt-6">
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white text-gray-500">
                Need help?
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}



function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userName, setUserName] = useState('');

  return (
    <Router>
      <div className ="app-container"> 
      <Routes>
        <Route
          path="/"
          element={
            isAuthenticated ? <Navigate to="/fileupload" replace /> : <SignIn setIsAuthenticated={setIsAuthenticated} setUserName={setUserName}/>
          }
        />
        <Route path="/fileupload" element={isAuthenticated ? <FileUpload /> : <Navigate to="/" replace />} />
        <Route path="/operations" element={isAuthenticated ? <OperationsPage /> : <Navigate to="/" replace />} />
        <Route path="/comment" element={isAuthenticated ? <CommentPage /> : <Navigate to="/" replace />} />
        <Route path="/commentLoad" element={isAuthenticated ? <CommentLoad /> : <Navigate to="/" replace />} />
        <Route path="/logs" element={isAuthenticated ? <ReportPage /> : <Navigate to="/" replace />} />
        <Route path="/calendar" element={<Calendar />} /> {/* Add this line */}
      </Routes>
      </div>
    </Router>
  );
}

export default App;
