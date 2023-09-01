import React from "react";
import { Link } from 'react-router-dom';
import "../Styles/Footer.css"

const Footer = () => {
    return (
        <div className="DivFooter">
            <Link to="/aboutus">About us</Link>
            <p>Your Text Here</p>
            <a href="https://github.com/JulienGha" target="_blank" rel="noopener noreferrer">GitHub</a>
        </div>
    )
}
export default Footer;
