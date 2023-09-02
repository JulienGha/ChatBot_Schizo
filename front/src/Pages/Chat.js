import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import Navbar from '../Components/Navbar';
import Footer from '../Components/Footer';
import axios from 'axios';
import '../Styles/Chat.css';

const ChatbotInterface = () => {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const params = useParams();

    const chatWindowRef = useRef(null);

    useEffect(() => {
        // Auto-scroll to the bottom of the chat window
        if (chatWindowRef.current) {
            chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
        }
    }, [messages]);

    useEffect(() => {
        // Your code to send a request to the server and validate the credential.
        // If validated, retrieve chat information.
        const fetchChatInfo = async () => {
            const Request = {
                method: 'get',
                url: `http://localhost:5000/get_messages?chat_id=${params.chat_id}`,
                withCredentials: true,
            };
            await axios(Request)
                .then(response => {
                    setMessages(response.data.messages)
                }) 
                .catch(error => {
                    console.log(error);
                });
        };
        fetchChatInfo();
    }, [params.chat_id]);

    const handleSendMessage = () => {
        if (inputMessage.trim() === '') return;
        const profileRequest = {
            method: 'post',
            url: `http://localhost:5000/post_messages`,
            withCredentials: true,
            data: {
                chat_id: params.chat_id,
                message: inputMessage,
            },
        };

        axios(profileRequest)
            .then(response => {
                const newMessages = [...messages, { content: inputMessage, user: 'user', date: response.data.date }];
                setMessages(newMessages);
                setInputMessage('');
            })
            .catch(error => {
                console.log(error);
            });
    };

    const handleFormSubmit = (e) => {
        e.preventDefault(); // Prevent the form from refreshing the page

        handleSendMessage();
    };

    const handleTestCredential = () => {
        const profileRequest = {
            method: 'post',
            url: `http://localhost:5000/test_cookie`,
            withCredentials: true,
            data: {
                chat_id: params.chat_id,
            },
        };

        axios(profileRequest)
            .then(response => {
                alert(response.status); // Log the response data
            })
            .catch(error => {
                console.log(error);
            });
    };

    return (
        <div>
            <Navbar></Navbar>
            <div className="ChatPage">
                <div className="chat-window" ref={chatWindowRef}>
                    <h1>Chatbot Interface for Chat ID: {params.chat_id}</h1>
                    {messages.map((message, index) => (
                        <div key={index} className={`message ${message.user}`}>
                            {message.content}
                        </div>
                    ))}
                </div>
                <div className="input-area">
                <form className="input-area" onSubmit={handleFormSubmit}>
                    <input
                        type="text"
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        placeholder="Type your message..."
                    />
                    <button type="submit">Send</button>
                </form>
                </div>
                <button onClick={handleTestCredential}>Test Cookie</button>
            </div>
            <Footer></Footer>
        </div>
    );
};

export default ChatbotInterface;
