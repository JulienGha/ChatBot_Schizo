import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import Navbar from '../Components/Navbar';
import Footer from '../Components/Footer';
import axios from 'axios';
import '../Styles/Chat.css'

const ChatbotInterface = () => {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const params = useParams()

    const handleSendMessage = () => {
        if (inputMessage.trim() === '') return;

        // Add user message to the chat
        setMessages([...messages, { text: inputMessage, type: 'user' }]);

        // Simulate chatbot response (replace with actual response logic)
        const chatbotResponse = "Hello! How can I assist you today?";
        setMessages([...messages, { text: chatbotResponse, type: 'bot' }]);

        // Clear input field
        setInputMessage('');
    };


    const handleTestCredential = () => {
        const profileRequest = {
            method: 'post',
            url: `http://localhost:5000/test_cookie`,
            withCredentials: true,
            data: {
                chatId: params.chat_id,
              },
        };

        axios(profileRequest)
            .then(response => {
                console.log(response.data); // Log the response data
            })
            .catch(error => {
                console.log(error);
            });
    };

    return (
        <div>
            <Navbar></Navbar>
            <div className="ChatPage">
                <div className="chat-window">
                    <h1>Chatbot Interface for Chat ID: {params.chat_id}</h1>
                    {messages.map((message, index) => (
                        <div key={index} className={`message ${message.type}`}>
                            {message.text}
                        </div>
                    ))}
                </div>
                <div className="input-area">
                    <input
                        type="text"
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        placeholder="Type your message..."
                    />
                    <button onClick={handleSendMessage}>Send</button>
                </div>
                <button onClick={handleTestCredential}>test cookie</button>
            </div>
            <Footer></Footer>
        </div>
    );
};

export default ChatbotInterface;
