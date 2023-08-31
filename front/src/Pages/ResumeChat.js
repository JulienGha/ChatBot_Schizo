import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import axios from 'axios';
import Navbar from '../Components/Navbar';
import Footer from '../Components/Footer';
import '../Styles/Resume.css'

const ResumeChatPage = () => {
  const history = useHistory();
  const [chatId, setChatId] = useState('');
  const [password, setPassword] = useState('');

  const handleResumeChat = async () => {
    try {
      var SignatureRequest = {
        method: 'post',
        url: `http://localhost:5000/resume`,
        data: {
            chatId: chatId,
            password: password,
        },
    };
    await axios(SignatureRequest)
        .then(response => {
            console.log(response)
            history.push(`/chat/${chatId}`)
        })
      } catch (error) {
        console.log(error)
      }
  };

  return (
    <div>
      <Navbar></Navbar>
      <div className='ResumePage'>
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
