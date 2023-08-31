import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import Navbar from '../Components/Navbar';
import Footer from '../Components/Footer';
import "../Styles/Create.css"
import axios from 'axios';

const CreateChatPage = () => {
  const history = useHistory();
  const [password, setPassword] = useState('');
  const [chatId, setChatId] = useState('');

  const handleCreateChat = async () => {
    try {
    var SignatureRequest = {
      method: 'post',
      url: `http://localhost:5000/create`,
      data: {
          password: password,
      },
  };
  await axios(SignatureRequest)
      .then(response => {
          setChatId(response.data.chatId)
          console.log(response)
          history.push(`/chat/${response.data.chatId}`)
      })
    } catch (error) {
      console.log(error)
    }
  };


  return (
    <div>
      <Navbar></Navbar>
      <div className='CreatePage'>
        <input
          type="password"
          placeholder="Set Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleCreateChat}>Create Chat</button>
        {chatId}
      </div>
      <Footer></Footer>
    </div>
  );
};

export default CreateChatPage;
