import React, { useState, useEffect } from 'react';
import Layout from './dashboard'; 


const ReportPage = () => {
  const [fileContent, setFileContent] = useState('');
  const [error, setError] = useState(false);

  useEffect(() => {
    // Fetching the file from the Flask backend
    fetch('http://localhost:3000/get-comments')
      .then((response) => {
        // Check if the response is okay (status 200-299)
        if (!response.ok) {
          throw new Error('Failed to load file');
        }
        return response.text();
      })
      .then((data) => setFileContent(data))
      .catch((error) => {
        console.error('Error loading file:', error);
        setError(true); // Set error state if fetching fails
      });
  }, []); // Empty dependency array ensures this runs once on component mount

  return (
    <Layout> 
    <div className="bg-gray-900 flex flex-col items-center py-8 h-screen w-screen">
      <div className="w-full max-w-4xl bg-gray-400 shadow-md rounded-lg p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-4">Log Content</h1>
        <pre
          className="bg-gray-300 p-4 border border-gray-300 rounded-md text-sm text-gray-700 overflow-y-auto max-h-96 whitespace-pre-wrap"
          role="document"
          aria-label="Report content"
        >
          {error ? 'Error loading file. Please try again later.' : fileContent || 'Loading...'}
        </pre>
      </div>
    </div>
    </Layout>
  );
};

export default ReportPage;
