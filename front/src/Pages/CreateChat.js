import React, { useState } from 'react';
import Navbar from '../Components/Navbar';
import Footer from '../Components/Footer';
import axios from 'axios';

const CreateChatPage = () => {
  const [password, setPassword] = useState('');
  const [chatId, setChatId] = useState('');

  const handleCreateChat = () => {
    // Send request to server for creating a new chat with password
    // Server generates a unique chat ID and returns it
    // Update the state with the generated chat ID
  };

  return (
    <div>
      <Navbar></Navbar>
      <div>
        <input
          type="password"
          placeholder="Set Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleCreateChat}>Create Chat</button>
        {chatId && <p>Your Chat ID: {chatId}</p>}
      </div>
      <Footer></Footer>
    </div>
  );
};

export default CreateChatPage;
