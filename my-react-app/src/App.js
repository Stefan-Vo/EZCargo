import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import './App.css'; 

function SignIn({ setIsAuthenticated }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSignIn = (e) => {
    e.preventDefault();
    if (username === 'admin' && password === 'password') {
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
  const [comment, setComment] = useState('');

  const handleCommentSubmit = () => {
    if (comment.trim() === '') {
      alert('Please type a comment before submitting!');
      return;
    }
    alert(`Your comment has been submitted: "${comment}"`);
    setComment(''); 
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100vh', 
      }}
    >
      <div style={{ flex: 1 }}>
        <h1>EZCargo Algorithms</h1>
        {/*  */}
      </div>

      <div
        style={{
          padding: '10px',
          borderTop: '1px solid #ddd',
          backgroundColor: '#f9f9f9',
        }}
      >
        <textarea
          placeholder="Add your comments here..."
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          style={{
            width: '200%',
            height: '100px',
            marginBottom: '10px',
            padding: '10px',
            borderRadius: '5px',
            border: '1px solid #ddd',
            fontSize: '16px',
          }}
        />
        <br />
        <button
          onClick={handleCommentSubmit}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            borderRadius: '5px',
            border: 'none',
            backgroundColor: '#4CAF50',
            color: 'white',
            cursor: 'pointer',
          }}
        >
          Submit Comment
        </button>
      </div>
    </div>
  );
}



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
