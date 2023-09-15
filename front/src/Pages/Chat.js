import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import Navbar from '../Components/Navbar';
import Footer from '../Components/Footer';
import axios from 'axios';
import '../Styles/Chat.css';
import "../Styles/AllStyle.css"


const ChatbotInterface = () => {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [lock, setLock] = useState(false)
    const [chatPurpose, setChatPurpose] = useState('')
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
                    setChatPurpose(response.data.chatPurpose)
                })
                .catch(error => {
                    console.log(error);
                });
        };
        fetchChatInfo();
    }, [params.chat_id]);

    const handleSendMessage = () => {
        if (inputMessage.trim() === '') return;
        setLock(true)
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
                const newMessages = []
                response.data.messages.forEach(message => {
                    newMessages.push({ content: message.content, user: message.user, date: message.date });
                }); 
                setMessages([...messages, newMessages[0], newMessages[1]]);
                setInputMessage('');
                setLock(false)
            })
            .catch(error => {
                console.log(error);
            });
    };

    const handleFormSubmit = (e) => {
        e.preventDefault(); // Prevent the form from refreshing the page
        handleSendMessage();
    };


    return (
        <div>
            <Navbar></Navbar>
            <div className="ChatPage">
                <div className="chat-window" ref={chatWindowRef}>
                    <h1>Chat ID: {params.chat_id} Chat type: {chatPurpose}</h1>
                    {messages.length > 0 && messages.map((message, index) => (
                        <div key={index} className={`message ${message.user}`}>
                            {message.content}
                        </div>
                    ))}
                </div>
                <div className="input-area">
                    <form onSubmit={handleFormSubmit} className='form-area'>
                        <input
                            type="text"
                            value={inputMessage}
                            onChange={(e) => setInputMessage(e.target.value)}
                            placeholder="Type your message..."
                        />
                        {(!lock) ? <button style={{"padding": "30px 20px"}} type="submit">Send</button>:
                        <></>}
                        
                    </form>
                </div>
            </div>
            <Footer></Footer>
        </div>
    );
};

export default ChatbotInterface;
