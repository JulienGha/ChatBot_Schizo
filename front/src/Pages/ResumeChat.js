import React, { useState } from 'react';
import axios from 'axios';
import Navbar from '../Components/Navbar';
import Footer from '../Components/Footer';
import '../Styles/Resume.css'

const ResumeChatPage = () => {
  const [chat_id, setChatId] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault();
    handleResumeChat();
  };

  const handleResumeChat = async () => {
    try {
      var SignatureRequest = {
        method: 'post',
        url: `http://localhost:5000/resume`,
        data: {
          chat_id: chat_id,
          password: password,
        },
      };
      await axios(SignatureRequest)
        .then(response => {
          if (response.status === 200) {
            document.cookie = `authToken=${response.data.token}; expires=${new Date(response.data.exp * 1000).toUTCString()}; path=/`;
            window.location.replace("/chat/" + chat_id, { replace: false });
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
        <form onSubmit={handleSubmit} className='form-container'>
          <input
            type="text"
            placeholder="Chat ID"
            value={chat_id}
            onChange={(e) => setChatId(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit">Resume Chat</button>
        </form>
        {errorMsg && <p>{errorMsg}</p>}
      </div>
      <Footer></Footer>
    </div>
  );
};

export default ResumeChatPage;
