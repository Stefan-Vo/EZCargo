import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Layout from './dashboard';
import './App.css';

function CommentPage({ username }) {
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

  const [containersToLoad, setContainersToLoad] = useState(""); // How many containers
  const [containerModals, setContainerModals] = useState([]); // Track multiple modals
  const [containerName, setContainerName] = useState(""); // New container name
  const [containerWeight, setContainerWeight] = useState(""); // New container weight

  const navigate = useNavigate(); // Initialize useNavigate hook for navigation

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

  // Handle change for the "How many containers do you want to load" input
  const handleContainersChange = (e) => {
    const value = e.target.value;
    if (value === "" || /^[0-9]*$/.test(value)) {
      setContainersToLoad(value);
    }
  };

  // Open multiple modals based on user input for container load
  const handleEnterButtonClick = () => {
    if (!containersToLoad) {
      alert("Please enter the number of containers to load!");
      return;
    }

    const modalsToOpen = Array.from({ length: parseInt(containersToLoad, 10) });
    setContainerModals(modalsToOpen); // Open the number of modals specified
  };

  // Handle the creation of a new container (for each modal)
  const handleCreateContainer = async (index) => {
    if (containerName.trim() && containerWeight.trim()) {
      // Log the new container data for now (you can replace this with your gridItems or API logic)
      console.log(`New container ${index + 1}:`, containerName, containerWeight);
    
      // Send the container data to the backend
      try {
        const response = await axios.post("http://localhost:5000/create-container-file", {
          containers: [{ name: containerName, weight: containerWeight }],
        });
    
        if (response.status === 200) {
          alert("Container added successfully to the file!");
          setContainerModals((prev) => prev.filter((_, i) => i !== index)); // Remove modal after creation
          setContainerName(""); // Reset input fields
          setContainerWeight(""); // Reset input fields
        } else {
          alert("Failed to add the container to the file.");
        }
      } catch (error) {
        console.error("Error adding container to file:", error);
        alert("An error occurred while adding the container.");
      }
    } else {
      alert("Please fill in both Container Name and Weight.");
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

        {/* Display the username entered during SignIn */}
        <div className="comment-author">
          <p className="text-xl font-semibold text-center text-white">{username}</p>
        </div>

        {/* Section with both the container input box and the comment textarea */}
        <div className="comment-section mt-6 flex justify-between items-start">
          {/* Left side: "How many containers do you want to load?" */}
          <div className="flex-1 mr-4">
            <label className="text-white font-semibold mb-2 block" htmlFor="containers-to-load">
              How many containers do you want to load?
            </label>
            <input
              id="containers-to-load"
              type="number"
              className="bg-cyan-950 text-white border-2 border-gray-300 p-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 w-full"
              placeholder="Enter number"
              value={containersToLoad}
              onChange={handleContainersChange}
            />
            <button
              onClick={handleEnterButtonClick}
              className="mt-2 bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 w-full"
            >
              Enter
            </button>
          </div>

          {/* Right side: Comment textarea */}
          <div className="flex-1 ml-4">
            <textarea
              className="bg-cyan-950 text-white border-2 border-gray-300 p-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 w-full"
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
        </div>

        {/* "Next Move" Button */}
        <div className="flex-shrink-0 mt-4">
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
            style={{
              position: 'absolute',
              bottom: '60px',
              right: '300px',
              width: '250px',
              height: '00px'
            }}
          >
            Next Move
          </button>
        </div>

        {/* Modal for creating containers */}
        {containerModals.map((_, index) => (
          <div key={index} className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
            <div className="bg-white p-6 rounded-lg shadow-lg w-80">
              <h2 className="text-lg font-semibold mb-4">Create New Container {index + 1}</h2>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Container Name</label>
                <input
                  type="text"
                  className="border border-gray-300 rounded-md p-2 w-full"
                  value={containerName}
                  onChange={(e) => setContainerName(e.target.value)}
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Container Weight (kg)</label>
                <input
                  type="text"
                  className="border border-gray-300 rounded-md p-2 w-full"
                  value={containerWeight}
                  onChange={(e) => setContainerWeight(e.target.value)}
                />
              </div>

              <div className="flex justify-end mt-4">
                <button
                  className="bg-red-500 text-white px-4 py-2 rounded-md mr-2"
                  onClick={() => setContainerModals((prev) => prev.filter((_, i) => i !== index))}
                >
                  Cancel
                </button>
                <button
                  className="bg-blue-500 text-white px-4 py-2 rounded-md"
                  onClick={() => handleCreateContainer(index)}
                >
                  Create Container
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </Layout>
  );
}

export default CommentPage;
