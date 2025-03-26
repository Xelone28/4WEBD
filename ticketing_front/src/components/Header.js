import React, { useEffect, useState } from "react";
import "../css/Header.css";
import { useNavigate } from "react-router-dom";

const Header = () => {
    const navigate = useNavigate();

    return (
        <header className="header">
            <div className="header-content">
                <h2 className="logo">TicketTac</h2>
                <div className='header-links'>
                    <nav>
                        <ul>
                            <li onClick={() => { navigate("/"); }}>Billets</li>
                        </ul>
                    </nav>
                </div>
            </div>
        </header>
    );
};

export default Header;