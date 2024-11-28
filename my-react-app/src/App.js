import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import './App.css'; 
import axios from "axios";


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
      <h1 className="text-2xl font-bold text-black-900">Welcome to EZCargo</h1>
      <form onSubmit={handleSignIn} className="sign-in-form">
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



function CommentPage() {
  const [gridItems, setGridItems] = useState(
    Array.from({ length: 96 }, (_, index) => ({
      id: index + 1,
      name: `Name ${index + 1}`,
      weight: "",
    }))
  );

  const [comment, setComment] = useState("");

  const editName = (index) => {
    const newName = prompt("Enter a new name:", gridItems[index].name);
    if (newName && newName.trim() !== "") {
      setGridItems((prevItems) =>
        prevItems.map((item, i) =>
          i === index ? { ...item, name: newName } : item
        )
      );
    }
  };

  const handleWeightChange = (index, weight) => {
    setGridItems((prevItems) =>
      prevItems.map((item, i) =>
        i === index ? { ...item, weight } : item
      )
    );
  };

  const submitComment = async () => {
    if (!comment.trim()) {
      alert("Please type a comment before submitting!");
      return;
    }
  
    try {
      // Send the comment to the backend
      const response = await axios.post("http://localhost:5000/submit-comment", {comment,});
  
      if (response.status === 200) {
        alert("Comment submitted successfully!");
        setComment(""); // Clear the comment input
      } else {
        alert("Failed to submit the comment.");
      }
    } catch (error) {
      console.error("Error submitting comment:", error);
      alert("An error occurred while submitting the comment.");
    }
  };

  return (
    <div>
      <nav class="w-full bg-gray-800">
       <div class="flex items-center">
          <div class="shrink-0">
          </div>
          <div class="hidden md:block">
            <div class="ml-10 flex items-baseline space-x-4">
              <a href="#" class="rounded-md bg-gray-900 px-3 py-2 text-sm font-medium text-white" aria-current="page">Dashboard</a>
              <a href="#" class="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white">Calendar</a>
              <a href="#" class="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white">Reports</a>
            </div>
          </div>
        </div>
      </nav>

    <div className="app">
      {/* Add a header or menu */}
      <div className="header">
        <h1 className="text-4xl font-bold text-gray-800 leading-tight text-center">EZCargo</h1>

      </div>
  
      {/* Existing grid-container */}
      <div className="grid-container">
        {gridItems.map((item, index) => (
          <div className="grid-item" key={item.id}>
            <div
              className="name"
              onClick={() => editName(index)}
              role="button"
              tabIndex={0}
            >
              {item.name}
            </div>
            <input
              type="text"
              className="weight-input"
              placeholder="Weight (kg)"
              value={item.weight}
              onChange={(e) => handleWeightChange(index, e.target.value)}
            />
          </div>
        ))}
      </div>
  
      {/* Existing comment section */}
      <div className="comment-section">
        <textarea
          id="commentBox"
          placeholder="Type your comment here..."
          value={comment}
          onChange={(e) => setComment(e.target.value)}
        ></textarea>
        <button onClick={submitComment}>Submit Comment</button>
      </div>
    </div>
  </div>
  );
  
};




function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <Router>
      <div className="app-container">
        <Routes>
          <Route
            path="/"
            element={
              isAuthenticated ? (
                <Navigate to="/comment" replace />
              ) : (
                <SignIn setIsAuthenticated={setIsAuthenticated} />
              )
            }
          />
          <Route
            path="/comment"
            element={
              isAuthenticated ? (
                <CommentPage />
              ) : (
                <Navigate to="/" replace />
              )
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
