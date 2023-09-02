import React from "react";
import { Link } from 'react-router-dom';
import "../Styles/Footer.css"

const Footer = () => {
    return (
        <div className="DivFooter">
            <Link to="/aboutus">About us</Link>
            <p></p>
            <div style={{justifyContent:"space-evenly", height:"100%", display:"flex", flexDirection:"column"}}>
                <a href="https://github.com/JulienGha" target="_blank" rel="noopener noreferrer">GitHub</a>
                <p>@Nagoya Institute of Technology</p>
            </div>
            
        </div>
    )
}
export default Footer;
