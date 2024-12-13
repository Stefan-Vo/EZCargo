import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';  // Import useNavigate from react-router-dom

function TakeFile() {
  const [file, setFile] = useState();
  const navigate = useNavigate();  // Initialize useNavigate hook to programmatically navigate

  function handleChange(event) {
    const selectedFile = event.target.files[0];

    // Check if the selected file is a .txt file
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
        // Redirect to the "comments" page after a successful upload
        navigate('/comment');
      })
      .catch((error) => {
        console.error('There was an error uploading the file!', error); // Error handling
      });
  }

  return (
    <div className="App">
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

export default TakeFile;
