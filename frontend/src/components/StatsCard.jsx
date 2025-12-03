import React from 'react';
import './StatsCard.css';

function StatsCard({ title, value, icon, color }) {
  return (
    <div className="stats-card" style={{ borderLeftColor: color }}>
      <div className="stats-icon" style={{ background: color }}>
        {icon}
      </div>
      <div className="stats-content">
        <div className="stats-title">{title}</div>
        <div className="stats-value">{value.toLocaleString()}</div>
      </div>
    </div>
  );
}

export default StatsCard;
