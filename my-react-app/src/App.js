import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [numbers, setNumbers] = useState([]);
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://localhost:5000/run-algorithm', {
        numbers: numbers.map(Number), // Send numbers as JSON
      });
      setResult(response.data.output); // Display result
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>EZCargo Algorithms</h1>
      <input
        type="text"
        placeholder="In Development"
        onChange={(e) => setNumbers(e.target.value.split(','))}
      />
      <button onClick={handleSubmit}>Deploy</button>
      {result !== null && <h2>Result: {result}</h2>}
    </div>
  );
}

export default App;