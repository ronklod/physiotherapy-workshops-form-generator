import React from 'react';
import './Header.css';
import logo from '../images/logo.png';

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-title-container">
          <h1 className="header-title">מחולל טופס התעמלות פיזיותרפיה</h1>
          <div className="header-logo-container">
            <img src={logo} alt="Logo" className="header-logo" />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header; 