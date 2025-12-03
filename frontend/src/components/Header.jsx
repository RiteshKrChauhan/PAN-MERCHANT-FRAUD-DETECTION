import React from 'react';
import { useNavigate } from 'react-router-dom';
import SearchBar from './SearchBar.jsx';
import './Header.css';

function Header() {
  const navigate = useNavigate();

  return (
    <header className="header">
      <div className="header-container">
        <div className="header-left" onClick={() => navigate('/')}>
          <h1 className="header-title">
            <span className="icon">🛡️</span>
            PAN Merchant Fraud Detection
          </h1>
        </div>
        <div className="header-right">
          <SearchBar />
        </div>
      </div>
    </header>
  );
}

export default Header;
