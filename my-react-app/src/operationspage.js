import React from 'react';
import { useNavigate } from 'react-router-dom';

function OperationsPage() {
    const navigate = useNavigate();

    const handleLoadUnload = () => {
        navigate('/commentLoad'); 
    };

    const handleBalance = () => {
        navigate('/comment'); 
    };

    return (
        <div className="app">
            <div className="header">
            <h1 className="text-4xl font-bold text-white leading-tight text-center">EZCargo</h1>
            </div>
            <div className="bg-gray-900 flex flex-col items-center py-8 h-screen w-screen">

                <div className="">
                    <div className="bg-gray-500 p-8 rounded-lg shadow-md w-full max-w-md">
                        <h2 className="text-2xl font-bold text-center text-gray-800 mb-8">
                            Container Operations
                        </h2>
                        
                        <div className="space-y-4">
                            <button
                                onClick={handleLoadUnload}
                                className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-600 transition duration-300 ease-in-out transform hover:scale-105"
                            >
                                Load/Unload
                            </button>
                            
                            <button
                                onClick={handleBalance}
                                className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-green-600 transition duration-300 ease-in-out transform hover:scale-105"
                            >
                                Balance
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default OperationsPage;