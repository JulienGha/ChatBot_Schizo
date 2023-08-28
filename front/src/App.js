import React from 'react';
import {Route, Routes} from 'react-router-dom'
import CreateChatPage from './Pages/CreateChat';
import HomePage from './Pages/Home';
import ResumeChatPage from './Pages/ResumeChat';
import ChatbotInterface from './Pages/Chat';

function App() {

  return (
      <Routes>
          <Route exact path="*" element={<HomePage/>}/>
          <Route exact path="/create" element={<CreateChatPage/>}/>
          <Route exact path="/resume" element={<ResumeChatPage/>}/>
          <Route path="/chat/:chat_id" element={<ChatbotInterface/>}/>
      </Routes>
  );
}

export default App;

