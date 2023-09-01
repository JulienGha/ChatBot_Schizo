import React, { useState } from 'react';
import axios from 'axios';
import Navbar from '../Components/Navbar';
import Footer from '../Components/Footer';
import '../Styles/Resume.css'

const ResumeChatPage = () => {
  const [chatId, setChatId] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('')

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
          if (response.status === 200) {
            document.cookie = `authToken=${response.data.token}; expires=${new Date(response.data.exp * 1000).toUTCString()}; path=/`;
            window.location.replace("/chat/" + chatId, { replace: false });
          }
        })
        .catch(error => {
          setErrorMsg(error.response.data.message)
        })
    } catch (error) {
      console.log(error)
    }
  };

  return (
    <div>
      <Navbar></Navbar>
      <div className='ResumePage'>
        <p className='explanation'>
          If you already have a chat session, please enter your Chat ID and Password. The Chat ID was provided when you created the chat.
        </p>
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
        <p>{errorMsg}</p>
        <button onClick={handleResumeChat}>Resume Chat</button>
      </div>
      <Footer></Footer>
    </div>
  );
};

export default ResumeChatPage;
