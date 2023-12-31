import React, { useState } from 'react';
import Navbar from '../Components/Navbar';
import Footer from '../Components/Footer';
import axios from 'axios';
import "../Styles/Create.css"
import "../Styles/AllStyle.css"


const CreateChatPage = () => {
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [chatPurpose, setChatPurpose] = useState('knowledge');


  const handleSubmit = async (e) => {
    e.preventDefault();
    handleCreateChat();
  };

  const handleCreateChat = async () => {
    try {
      var SignatureRequest = {
        method: 'post',
        url: `http://localhost:5000/create`,
        data: {
          password: password,
          chatPurpose: chatPurpose,
        },
      };
      await axios(SignatureRequest)
        .then(response => {
          if (response.status === 200) {
            document.cookie = `authToken=${response.data.token}; expires=${new Date(response.data.exp).toUTCString()}; path=/`;
            window.location.replace("/chat/" + response.data.chat_id, { replace: false });
          }
        })
        .catch(error => {
          setErrorMsg(error)
        })
    } catch (error) {
      console.log(error)
    }
  };


  return (

    <div>
      <Navbar></Navbar>
      <div className='CreatePage'>
        <div className="explanation">
          <p>
            In order to ensure your anonymity, we do not require an account to use this service.
            Instead, we ask you to set a password. Upon creating a chat, you'll be provided with
            a unique Chat ID. To re-access your chat, you'll need both this Chat ID and the password you set.
          </p>
        </div>
        <form onSubmit={handleSubmit} className='form-container'>
          <div className="chat-purpose-toggle">
            <label className={chatPurpose === 'knowledge' ? 'active' : ''}>
              <input
                type="radio"
                value="knowledge"
                checked={chatPurpose === 'knowledge'}
                onChange={(e) => setChatPurpose(e.target.value)}
              />
              Get knowledge about schizophrenia
            </label>
            <label className={chatPurpose === 'assistance' ? 'active' : ''}>
              <input
                type="radio"
                value="assistance"
                checked={chatPurpose === 'assistance'}
                onChange={(e) => setChatPurpose(e.target.value)}
              />
              Seek assistance
            </label>
          </div>
          <input
            type="password"
            placeholder="Set Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="your-input-class"  // Your original input class here
          />
          <button type="submit" className="button">Create Chat</button>
        </form>
        {errorMsg && <div className="error">{errorMsg}</div>}
      </div>
      <Footer></Footer>
    </div>
  );
};

export default CreateChatPage;
