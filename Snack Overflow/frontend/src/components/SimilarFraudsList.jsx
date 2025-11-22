import React from 'react';
import { useNavigate } from 'react-router-dom';
import './SimilarFraudsList.css';

function SimilarFraudsList({ frauds }) {
  const navigate = useNavigate();

  return (
    <div className="similar-frauds-list">
      <div className="frauds-table">
        <div className="table-header">
          <div className="table-cell">Rank</div>
          <div className="table-cell">Merchant ID</div>
          <div className="table-cell">Similarity</div>
          <div className="table-cell">PAN Hash</div>
          <div className="table-cell">Tier</div>
          <div className="table-cell">City</div>
          <div className="table-cell">Chargeback Rate</div>
          <div className="table-cell">Action</div>
        </div>
        
        {frauds.map((fraud, index) => (
          <div key={fraud.merchant_id} className="table-row">
            <div className="table-cell rank">#{index + 1}</div>
            <div className="table-cell merchant-id">{fraud.merchant_id}</div>
            <div className="table-cell">
              <div className="similarity-badge">
                {(fraud.similarity_score * 100).toFixed(1)}%
              </div>
            </div>
            <div className="table-cell">{fraud.pan_hash}</div>
            <div className="table-cell">
              <span className="tier-badge">{fraud.merchant_tier}</span>
            </div>
            <div className="table-cell">{fraud.city}</div>
            <div className="table-cell">
              {(fraud.chargeback_rate * 100).toFixed(2)}%
            </div>
            <div className="table-cell">
              <button
                className="view-button"
                onClick={() => navigate(`/merchant/${fraud.merchant_id}`)}
              >
                View Details
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SimilarFraudsList;
