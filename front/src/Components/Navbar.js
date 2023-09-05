import React from "react";
import { Link } from 'react-router-dom';
import axios from "axios";
import "../Styles/Navbar.css"
import "../Styles/AllStyle.css"

const Navbar = () => {

    const handleCreateChat = async () => {
        try {
          const response = await axios.get(`http://localhost:5000/test`);
          alert(response.status)
        } catch (error) {
          console.log(error)
        }
    };

    return (
        <div className="containerNavBar">
            <nav className="DivNavbar">
                <Link to="/">Hermegency</Link>  {/* Updated link to home */}
                <button onClick={handleCreateChat}>Server test</button>
            </nav>
        </div>
    )
}
export default Navbar;
