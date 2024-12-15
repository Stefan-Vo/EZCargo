import React, { useState, useEffect } from 'react';
import axios from "axios";
import Layout from './dashboard'; 
import './App.css'; 

function CommentLoad() {
  const [gridItems, setGridItems] = useState(
    Array.from({ length: 96 }, (_, index) => ({
      id: index + 1,
      name: `Name ${index + 1}`,
      weight: '0 Lbs: ',
    }))
  );

  const [comment, setComment] = useState("");
  const [comments, setComments] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(null);
  const [newName, setNewName] = useState("");
  const [newWeight, setNewWeight] = useState("");
  const [ship, setShip] = useState("SHIP1");
  const [isBalancing, setIsBalancing] = useState(false);

  useEffect(() => {
    const fetchComments = async () => {
      try {
        const response = await axios.get("http://localhost:5000/get-comments");
        if (response.status === 200) {
          setComments(response.data || []);
        }
      } catch (error) {
        console.error("Error fetching comments:", error);
        setComments([]);
      }
    };

    fetchComments();
  }, []);

  const handleBalance = async () => {
    try {
      setIsBalancing(true);
      
      // Convert grid items to the format expected by the backend
      const cellList = gridItems.map((item, index) => {
        const row = Math.floor(index / 12) + 1;
        const column = (index % 12) + 1;
        return {
          row: row,
          column: column,
          weight: parseInt(item.weight.replace(' Lbs: ', '')) || 0,
          name: item.name
        };
      });
  
      console.log("Sending to backend:", cellList); // Debug log
  
      const response = await axios.post("http://localhost:5000/balance", {
        ship: "SHIP1",
        cellList: cellList,
        bufferList: []
      });
  
      if (response.status === 200) {
        console.log("Received from backend:", response.data); // Debug log
        
        // Create a new array with the same length as gridItems
        const newGridItems = Array.from({ length: gridItems.length }, (_, index) => {
          const balancedItem = response.data.find(item => item.id === index + 1);
          if (balancedItem) {
            return {
              id: index + 1,
              name: balancedItem.name,
              weight: balancedItem.weight
            };
          }
          return {
            id: index + 1,
            name: "UNUSED",
            weight: "0 Lbs: "
          };
        });
  
        console.log("Updating grid with:", newGridItems); // Debug log
        setGridItems(newGridItems);
        alert("Containers balanced successfully!");
      }
    } catch (error) {
      console.error("Error balancing containers:", error);
      alert("An error occurred while balancing containers.");
    } finally {
      setIsBalancing(false);
    }
  };

  const handleOpenModal = (index) => {
    setCurrentIndex(index);
    setNewName(gridItems[index].name);
    setNewWeight(gridItems[index].weight);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setCurrentIndex(null);
    setNewName("");
    setNewWeight("");
  };

  const handleSaveChanges = () => {
    if (newName.trim() !== "" && newWeight.trim() !== "") {
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
      alert("Please type a comment before submitting!");
      return;
    }

    const timestamp = new Date().toLocaleString();

    try {
      const response = await axios.post("http://localhost:5000/submit-comment", {
        text: comment,
        timestamp: timestamp
      });
      
      if (response.status === 200) {
        setComments(prevComments => [...prevComments, {
          text: comment,
          timestamp: timestamp
        }]);
        setComment("");
      }
    } catch (error) {
      console.error("Error submitting comment:", error);
      alert("An error occurred while submitting the comment.");
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
            <div className="grid-item bg-cyan-950" key={item.id}>
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
            </div>
          ))}
        </div>

        <div className="flex justify-between gap-5 m-5">
          <div className="comment-section">
            <textarea
              className="bg-cyan-950 text-white border-2 border-gray-300 p-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Type your comment here..."
              value={comment}
              onChange={(e) => setComment(e.target.value)}
            ></textarea>
            <button 
              className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
              onClick={submitComment}
            >
              Submit Comment
            </button>

            <div className="comments-list mt-4">
              {comments && comments.map((commentItem, index) => (
                <div key={index} className="comment-item bg-cyan-900 p-3 mb-2 rounded">
                  <p className="text-white">
                    {`${commentItem.timestamp} - ${commentItem.text}`}
                  </p>
                </div>
              ))}
            </div>
          </div>

          <div className="flex justify-center items-center my-4 gap-4">
          <button 
            className="px-16 py-8 text-xl font-bold bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
            onClick={handleBalance}
            disabled={isBalancing}
          >
            {isBalancing ? 'Loading...' : 'Load'}
          </button>
        </div>

          <div className="flex justify-center items-center my-4">
            <button className="px-16 py-8 text-xl font-bold bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">
              Next
            </button>
          </div>
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

export default CommentLoad;