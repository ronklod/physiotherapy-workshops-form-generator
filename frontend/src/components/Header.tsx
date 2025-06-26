import React from 'react';
import './Header.css';

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="header-content">
        <h1 className="header-title">מחולל טופס התעמלות פיזיותרפיה</h1>
        <p className="header-subtitle">Hebrew Physiotherapy Workshops Form Generator</p>
      </div>
    </header>
  );
};

export default Header; 