import React from 'react';
import Navbar from '../Components/Navbar';
import Footer from '../Components/Footer';
import '../Styles/Aboutus.css';
import "../Styles/AllStyle.css"


function Aboutus() {
    return (
        <div>
            <Navbar></Navbar>
            <div className='AboutusPage'>
                <h1>What is Hermegency?</h1>
                <p>
                    "Hermegency" is your dedicated mental health companion, utilizing the power of advanced AI technology to offer support and assistance whenever you need it.
                    Designed to be completely anonymous, Hermegency provides a safe space for users to seek help for their mental well-being.
                    Our app is built upon the knowledge acquired from large language models (LLMs), allowing it to understand and respond to a wide range of emotional concerns.
                    Whether you're looking for guidance, a listening ear, or coping strategies, Hermegency is here to provide valuable insights and support while respecting your privacy.
                    You can trust Hermegency to be your companion on your journey to better mental health.
                </p>
                <h1>Who are we?</h1>
                <p>
                    
                </p>
                <h1>How to ensure your privacy?</h1>
                <p>
                    
                </p>
            </div>
            <Footer></Footer>
        </div>
    );
}

export default Aboutus;
