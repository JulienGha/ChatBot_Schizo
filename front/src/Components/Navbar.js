import React from "react";
import { Link } from 'react-router-dom';
import axios from "axios";
import "../Styles/Navbar.css"


const Navbar = () => {

    const handleCreateChat = async () => {
        // Test function to see if the server is answering
        try {
          const response = await axios.get(`http://localhost:5000/test`);
          console.log(response)
        } catch (error) {
          console.log(error)
        }
      };


    return (
            <div className="DivNavbar">
                <Link to="*">Hermegency</Link>
                <button onClick={handleCreateChat}>Server test</button>
                <p></p>
            </div>
        )
}
export default Navbar