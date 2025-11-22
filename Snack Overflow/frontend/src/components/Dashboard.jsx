import React, { useState, useEffect } from 'react';
import axios from 'axios';
import FraudRingGraph from './FraudRingGraph.jsx';
import StatsCard from './StatsCard.jsx';
import './Dashboard.css';

function Dashboard() {
  const [fraudRings, setFraudRings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedRing, setSelectedRing] = useState(null);

  useEffect(() => {
    fetchFraudRings();
  }, []);

  const fetchFraudRings = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/dashboard/fraud-rings');
      
      if (response.data.success) {
        setFraudRings(response.data.rings);
        if (response.data.rings.length > 0) {
          setSelectedRing(response.data.rings[0]);
        }
      }
    } catch (err) {
      setError('Failed to load fraud rings. Please try again later.');
      console.error('Error fetching fraud rings:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading fraud detection data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="container">
        <div className="dashboard-header">
          <h2>Top Fraud Rings Dashboard</h2>
          <p className="subtitle">Visualization of the largest fraud networks detected</p>
        </div>

        {/* Stats Cards */}
        <div className="stats-grid">
          <StatsCard
            title="Total Fraud Rings"
            value={fraudRings.length}
            icon="🔗"
            color="#667eea"
          />
          <StatsCard
            title="Largest Ring Size"
            value={fraudRings.length > 0 ? fraudRings[0].size : 0}
            icon="👥"
            color="#f093fb"
          />
          <StatsCard
            title="Total Fraudulent Merchants"
            value={fraudRings.reduce((sum, ring) => sum + ring.size, 0)}
            icon="⚠️"
            color="#4facfe"
          />
        </div>

        {/* Ring Selector */}
        <div className="card">
          <h3 className="card-title">Select Fraud Ring to Visualize</h3>
          <div className="ring-selector">
            {fraudRings.map((ring, index) => (
              <button
                key={ring.ring_id}
                className={`ring-button ${selectedRing?.ring_id === ring.ring_id ? 'active' : ''}`}
                onClick={() => setSelectedRing(ring)}
              >
                <div className="ring-button-title">Ring #{index + 1}</div>
                <div className="ring-button-size">{ring.size} merchants</div>
              </button>
            ))}
          </div>
        </div>

        {/* Graph Visualization */}
        {selectedRing && (
          <div className="card">
            <h3 className="card-title">
              Fraud Ring Network - {selectedRing.size} Merchants Connected
            </h3>
            <FraudRingGraph data={selectedRing} />
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
