import React, { useState } from 'react';
import './App.css';
import HebrewFormProcessor from './components/HebrewFormProcessor';
import Header from './components/Header';

function App() {
  return (
    <div className="App">
      <Header />
      <main className="main-content">
        <HebrewFormProcessor />
      </main>
    </div>
  );
}

export default App; 