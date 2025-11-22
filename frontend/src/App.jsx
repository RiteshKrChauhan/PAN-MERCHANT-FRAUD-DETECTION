import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard.jsx';
import MerchantDetails from './components/MerchantDetails.jsx';
import Header from './components/Header.jsx';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/merchant/:merchantId" element={<MerchantDetails />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
