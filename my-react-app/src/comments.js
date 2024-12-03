import React, { useState } from 'react';
import axios from "axios";
import Layout from './dashboard'; 
import './App.css'; 


function CommentPage() {
  const [gridItems, setGridItems] = useState(
    Array.from({ length: 96 }, (_, index) => ({
      id: index + 1,
      name: `Name ${index + 1}`,
      weight: '0 Lbs: ',
    }))
  );

  const [comment, setComment] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(null);
  const [newName, setNewName] = useState("");
  const [newWeight, setNewWeight] = useState("");

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

    try {
      const response = await axios.post("http://localhost:5000/submit-comment", { comment });
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
            </div>
          ))}
        </div>

        <div className="comment-section">
          <textarea
            className="bg-cyan-950 text-white border-2 border-gray-300 p-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Type your comment here..."
            value={comment}
            onChange={(e) => setComment(e.target.value)}
          ></textarea>
          <button onClick={submitComment}>Submit Comment</button>
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
