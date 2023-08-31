import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../Components/Navbar';
import Footer from '../Components/Footer';
import '../Styles/Home.css'

function HomePage() {
    return (
        <div>
            <Navbar></Navbar>
            <div className='HomePage'>
                <h1>Welcome to Hermegency</h1>
                <p>"Hermegency" is your dedicated mental health companion, utilizing the power of advanced AI technologies, like chatbot and large language models, to offer support and assistance whenever you need it.</p>
                <div className='ContentLinks'>
                    <Link to="/resume">Resume a Chat</Link>
                    <Link to="/create">Create a New Chat</Link>
                </div>
            </div>
            <Footer></Footer>
        </div>
    );
}

export default HomePage;

