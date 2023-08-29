import React, { useState } from 'react';
import Navbar from '../Components/Navbar';
import Footer from '../Components/Footer';
import axios from 'axios';

const CreateChatPage = () => {
  const [password, setPassword] = useState('');
  const [chatId, setChatId] = useState('');

  const handleCreateChat = async () => {
    // Test function to see if the server is answering
    try {
      const response = await axios.post(`http://localhost:5000/create`);
      setChatId(response.data.chatId)
      console.log(response)
    } catch (error) {
      console.log(error)
    }
  };


  return (
    <div>
      <Navbar></Navbar>
      <div>
        <div>
          <input
            type="password"
            placeholder="Set Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button onClick={handleCreateChat}>Create Chat</button>
        </div>
      </div>
      <Footer></Footer>
    </div>
  );
};

export default CreateChatPage;
