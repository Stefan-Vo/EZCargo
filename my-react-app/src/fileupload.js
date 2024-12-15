import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function FileUpload() {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setMessage('');
    };

    const handleUpload = async (e) => {
        e.preventDefault();
    
        if (!file) {
            setMessage('Please select a file first');
            return;
        }
    
        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);
    
        try {
            // Step 1: Upload the file
            const uploadResponse = await fetch('/upload-file', {
                method: 'POST',
                body: formData,
            });
    
            if (!uploadResponse.ok) {
                throw new Error(`HTTP error! status: ${uploadResponse.status}`);
            }
    
            const uploadData = await uploadResponse.json();
            const filename = uploadData.filename; // Extract filename
            if (!filename) {
                throw new Error("No filename returned by /upload-file");
            }
    
            // Step 2: Call process_upload with the filename
            const processResponse = await fetch('/process-upload', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ filename }),
            });
    
            if (!processResponse.ok) {
                throw new Error(`HTTP error! status: ${processResponse.status}`);
            }
    
            const processData = await processResponse.json();
            setMessage('File processed successfully!');
            console.log('Processed data:', processData);
    
            // Navigate to operations page after successful upload
            setTimeout(() => {
                navigate('/operations');
            }, 1000);
    
        } catch (error) {
            console.error('Error:', error);
            setMessage(`Operation failed: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
            <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">
                Upload Text File
            </h2>
            
            <form onSubmit={handleUpload} className="space-y-4">
                <div className="flex flex-col items-center">
                    <label 
                        className="w-full flex flex-col items-center px-4 py-6 bg-white text-blue-500 rounded-lg shadow-lg tracking-wide uppercase border border-blue-500 cursor-pointer hover:bg-blue-500 hover:text-white transition duration-300 ease-in-out"
                    >
                        <svg className="w-8 h-8" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                            <path d="M16.88 9.1A4 4 0 0 1 16 17H5a5 5 0 0 1-1-9.9V7a3 3 0 0 1 4.52-2.59A4.98 4.98 0 0 1 17 8c0 .38-.04.74-.12 1.1zM11 11h3l-4-4-4 4h3v3h2v-3z" />
                        </svg>
                        <span className="mt-2 text-sm">Select a text file</span>
                        <input 
                            type="file" 
                            accept=".txt"
                            onChange={handleFileChange}
                            className="hidden"
                        />
                    </label>
                    
                    {file && (
                        <span className="mt-2 text-sm text-gray-600">
                            Selected: {file.name}
                        </span>
                    )}
                </div>

                <button 
                    type="submit"
                    disabled={loading || !file}
                    className={`w-full px-4 py-2 text-white rounded-lg transition duration-300 ease-in-out ${
                        loading || !file 
                            ? 'bg-gray-400 cursor-not-allowed' 
                            : 'bg-blue-500 hover:bg-blue-600'
                    }`}
                >
                    {loading ? 'Uploading...' : 'Upload'}
                </button>
            </form>

            {message && (
                <div className={`mt-4 p-3 rounded-lg ${
                    message.includes('successfully') 
                        ? 'bg-green-100 text-green-700' 
                        : 'bg-red-100 text-red-700'
                }`}>
                    {message}
                </div>
            )}
        </div>
    );
}
export default FileUpload;