import React, { useState } from 'react';
import axios from 'axios';
import Navbar from '../Components/Navbar';
import Footer from '../Components/Footer';
import '../Styles/Resume.css'

const ResumeChatPage = () => {

  const [chatId, setChatId] = useState('');
  const [password, setPassword] = useState('');

  const handleResumeChat = () => {
    // Send request to server for resuming chat using chatId and password
  };

  return (
    <div>
      <Navbar></Navbar>
      <div>
        <input
          type="text"
          placeholder="Chat ID"
          value={chatId}
          onChange={(e) => setChatId(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleResumeChat}>Resume Chat</button>
      </div>
      <Footer></Footer>
    </div>
  );
};

export default ResumeChatPage;
