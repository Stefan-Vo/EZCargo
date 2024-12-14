import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Layout from './dashboard';
import './App.css';

function CommentPage({ username }) {
  const [gridItems, setGridItems] = useState([]);
  const [comment, setComment] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(null);
  const [newName, setNewName] = useState('');
  const [newWeight, setNewWeight] = useState('');

  useEffect(() => {
    const fetchManifestData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/get-manifest');
        
        if (response.status === 200 && response.data.data) {
          const manifestData = response.data.data;
          
          // Parse manifest data and flip the vertical coordinates
          const parsedItems = manifestData.trim().split('\n').map((line, index) => {
            const regex = /\[(\d{2}),(\d{2})\], \{(\d{5})\}, (.+)/;
            const match = line.match(regex);
            
            if (match) {
              const row = parseInt(match[1]);
              const col = parseInt(match[2]);
              // Flip the row number (1 becomes 8, 2 becomes 7, etc.)
              const flippedRow = 9 - row;
              
              return {
                id: index + 1,
                // Store both the original and flipped positions
                originalPosition: `${String(row).padStart(2, '0')},${String(col).padStart(2, '0')}`,
                position: `${String(flippedRow).padStart(2, '0')},${String(col).padStart(2, '0')}`,
                weight: match[3],
                name: match[4].trim()
              };
            }

            return null;
          }).filter(item => item !== null);

          // Sort items by flipped position: descending by row (8->1), ascending by column (1->12)
          const sortedItems = parsedItems.sort((a, b) => {
            const [aRow, aCol] = a.position.split(',').map(Number);
            const [bRow, bCol] = b.position.split(',').map(Number);
            if (aRow === bRow) {
              return aCol - bCol; // Sort by column within the same row
            }
            return aRow - bRow; // Sort by row (8->1)
          });

          setGridItems(sortedItems);
        }
      } catch (error) {
        console.error('Error fetching manifest data:', error);
        alert('An error occurred while fetching manifest data.');
      }
    };

    fetchManifestData();
  }, []);

  // Modal Handling
  const handleOpenModal = (index) => {
    setCurrentIndex(index);
    setNewName(gridItems[index].name);
    setNewWeight(gridItems[index].weight);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setCurrentIndex(null);
    setNewName('');
    setNewWeight('');
  };

  const handleSaveChanges = () => {
    if (newName.trim() !== '' && newWeight.trim() !== '') {
      setGridItems((prevItems) =>
        prevItems.map((item, i) =>
          i === currentIndex ? { ...item, name: newName, weight: newWeight } : item
        )
      );
      handleCloseModal();
    }
  };

  const submitComment = async () => {
    if (!comment.trim()) {
      alert('Please type a comment before submitting!');
      return;
    }

    try {
      const response = await axios.post('http://localhost:5000/submit-comment', { comment });
      if (response.status === 200) {
        alert('Comment submitted successfully!');
        setComment('');
      } else {
        alert('Failed to submit the comment.');
      }
    } catch (error) {
      console.error('Error submitting comment:', error);
      alert('An error occurred while submitting the comment.');
    }
  };
  class Container {
    constructor(id, weight) {
      this.id = id; 
      this.weight = weight; 
    }
  
    toString() {
      return `Container (${this.id}, ${this.weight})`;
    }
  
    getAttributes() {
      return [this.id, this.weight];
    }
  }
  const container = new Container("a", 500);
  console.log(container.toString()); // Output: Container (1, 500)
  console.log(container.getAttributes());
  class Cell {
    constructor(position, isFilled, container = null) {
      this.position = position; // [row, col]
      this.isFilled = isFilled; // boolean
      this.container = container; // Default is null
      this.h = Infinity;
      this.g = 0;
      this.totalCost = this.g + this.h;
    }
  }
  class Ship {
    constructor(matrix) {
      this.matrix = matrix; // 2D array representing the ship grid
      this.rows = matrix.length;
      this.columns = matrix[0].length;
      this.shipDict = {}; // Dictionary to hold container information
    }
  
    // Make the Ship iterable, yielding each row of the matrix
    [Symbol.iterator]() {
      let index = 0;
      return {
        next: () => {
          if (index < this.matrix.length) {
            return { value: this.matrix[index++], done: false };
          }
          return { done: true };
        }
      };
    }
    addContainer(position, container) {
      this.shipDict[position.toString()] = container;
    }
    displayContainers() {
      for (const [position, container] of Object.entries(this.shipDict)) {
        console.log(`Position: ${position}, Container: ${container}`);
      }
    }
  
    // Get the number of containers in the ship
    get length() {
      return Object.keys(this.shipDict).length;
    }
  }
  const handleBalanceConfirmation = async () => {
    const gridMatrix = Array(12).fill(0).map(() => Array(8).fill(0));
  
    const ship = {
      matrix: gridMatrix,
      rows: gridMatrix.length,
      columns: gridMatrix[0].length,
      shipDict: {},
    };
  
    const cellList = gridItems.map(item => ({
      position: item.position.split(',').map(Number),
      isFilled: true,
      container: item.name || null,
      weight: parseFloat(item.weight) || 0,
    }));
  
    const bufferList = [
      { position: [0, 0], isFilled: false, container: null },
      // Add mock buffer items or fetch dynamically if needed
    ];
  
    const data = { ship, cellList, bufferList };
  
    try {
      const response = await axios.post('http://localhost:5000/balance', data, {
        headers: { 'Content-Type': 'application/json' },
      });
  
      if (response.status === 200) {
        alert('Balance confirmed successfully!');
      } else {
        alert('Failed to confirm balance.');
      }
    } catch (error) {
      console.error('Error confirming balance:', error.response || error.message || error);
      alert('An error occurred while confirming the balance.');
    }
  };
  
  
  

  return (
    <Layout>
      <div className="app">
        <div className="header">
          <h1 className="text-4xl font-bold text-white leading-tight text-center">EZCargo</h1>
        </div>

        <div className="grid-container">
          {gridItems.map((item, index) => (
            <div className="grid-item" key={item.id}>
              <div
                className="name"
                onClick={() => handleOpenModal(index)}
                role="button"
                tabIndex={0}
              >
                {item.name}
              </div>
              <div
                className="weight"
                onClick={() => handleOpenModal(index)}
                role="button"
                tabIndex={0}
              >
                {item.weight}
              </div>
              <div className="position">
                <strong>Position:</strong> {item.originalPosition}
              </div>
            </div>
          ))}
        </div>

        <div className="comment-author">
          <p className="text-xl font-semibold text-center text-white">{username}</p>
        </div>

        <div className="comment-section mt-6 flex justify-between items-start">
          <div className="flex-1 mr-4">
            <textarea
              className="bg-cyan-950 text-white border-2 border-gray-300 p-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Type your comment here..."
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              style={{ marginTop: '10px' }}
            ></textarea>
            <button
              onClick={submitComment}
              className="mt-2 bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600"
            >
              Submit Comment
            </button>
          </div>

          <div className="flex-shrink-0 mt-4">
            <button
              className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
              style={{
                bottom: '60px',
                right: '300px',
                width: '250px',
                height: '100px'
              }}
            >
              Next Move
            </button>
          </div>
        </div>

        {/* Confirm Balance button - bottom left */}
        <div className="fixed bottom-0 left-0 mb-4 ml-4">
          <button
            className="bg-yellow-500 text-white px-4 py-2 rounded-md hover:bg-yellow-600"
            onClick={handleBalanceConfirmation}
          >
            Confirm Balance
          </button>
        </div>

        {isModalOpen && (
          <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
            <div className="bg-white p-6 rounded-lg shadow-lg w-80">
              <h2 className="text-lg font-semibold mb-4">Edit Item</h2>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                <input
                  type="text"
                  className="border border-gray-300 rounded-md p-2 w-full"
                  value={newName}
                  onChange={(e) => setNewName(e.target.value)}
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Weight (kg)</label>
                <input
                  type="text"
                  className="border border-gray-300 rounded-md p-2 w-full"
                  value={newWeight}
                  onChange={(e) => setNewWeight(e.target.value)}
                />
              </div>

              <div className="flex justify-end mt-4">
                <button
                  className="bg-red-500 text-white px-4 py-2 rounded-md mr-2"
                  onClick={handleCloseModal}
                >
                  Cancel
                </button>
                <button
                  className="bg-blue-500 text-white px-4 py-2 rounded-md"
                  onClick={handleSaveChanges}
                >
                  Save
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}

export default CommentPage;
