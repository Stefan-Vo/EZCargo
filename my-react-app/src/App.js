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
      <h1>Welcome to EZCargo</h1>
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
        <button type="submit" className="sign-in-button">
          Sign In
        </button>
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
    <div className="app">
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
