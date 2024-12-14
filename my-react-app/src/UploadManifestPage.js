import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, useLocation } from 'react-router-dom';  // Import useLocation to access the passed state

function UploadManifestPage() {
  const [file, setFile] = useState();
  const navigate = useNavigate();
  const location = useLocation();  // Access the passed state

  // Get the action from the state passed by App.js
  const action = location.state?.action;

  function handleChange(event) {
    const selectedFile = event.target.files[0];

    if (selectedFile && selectedFile.type !== 'text/plain') {
      alert('Please upload a .txt file');
      setFile(null); // Reset file state if the wrong file type is selected
      return;
    }

    setFile(selectedFile);
  }

  function handleSubmit(event) {
    event.preventDefault();

    if (!file) {
      alert('No file selected!');
      return;
    }

    const url = 'http://localhost:5000/upload-file';  // Ensure the URL is correct (Flask backend)

    const formData = new FormData();
    formData.append('file', file);

    const config = {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    };

    axios
      .post(url, formData, config)
      .then((response) => {
        console.log(response.data); // Success response

        // After a successful file upload, navigate to the correct page
        if (action === 'comment') {
          navigate('/comment');  // Go to the Comment Page
        } else if (action === 'load-unload') {
          navigate('/load-unload');  // Go to the Load/Unload Page
        }
      })
      .catch((error) => {
        console.error('There was an error uploading the file!', error); // Error handling
      });
  }

  return (
    <div className="app">
      <form onSubmit={handleSubmit}>
        <h1>React File Upload</h1>
        <input
          type="file"
          onChange={handleChange}
          accept=".txt"  // Restrict to .txt files
        />
        <button type="submit">Upload</button>
      </form>
    </div>
  );
}

export default UploadManifestPage;
