const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const axios = require('axios');
const path = require('path');

// Load .env from project root
require('dotenv').config({ path: path.join(__dirname, '..', '..', '..', '.env') });

const app = express();
const PORT = process.env.NODE_PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Python ML Service URL
const PYTHON_SERVICE_URL = process.env.PYTHON_SERVICE_URL || 'http://localhost:5000';

// ============================================================
// ROUTES
// ============================================================

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy', service: 'node-api-service' });
});

// Get top fraud rings for dashboard
app.get('/api/dashboard/fraud-rings', async (req, res) => {
  try {
    const response = await axios.get(`${PYTHON_SERVICE_URL}/api/top-fraud-rings`);
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching fraud rings:', error.message);
    
    res.status(500).json({
      success: false,
      error: 'Failed to fetch fraud rings',
      details: error.message
    });
  }
});

// Search merchant by ID
app.post('/api/search', async (req, res) => {
  try {
    const { merchant_id } = req.body;
    
    if (!merchant_id) {
      return res.status(400).json({
        success: false,
        error: 'Merchant ID is required'
      });
    }
    
    // Call Python service
    const response = await axios.post(`${PYTHON_SERVICE_URL}/api/search`, {
      merchant_id
    });
    
    res.json(response.data);
  } catch (error) {
    console.error('Error searching merchant:', error.message);
    
    res.status(error.response?.status || 500).json({
      success: false,
      error: 'Search failed',
      details: error.response?.data || error.message
    });
  }
});

// Get merchant details
app.get('/api/merchant/:merchant_id', async (req, res) => {
  try {
    const { merchant_id } = req.params;
    
    const response = await axios.get(`${PYTHON_SERVICE_URL}/api/merchant/${merchant_id}`);
    
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching merchant details:', error.message);
    
    res.status(error.response?.status || 500).json({
      success: false,
      error: 'Failed to fetch merchant details',
      details: error.response?.data || error.message
    });
  }
});

// Get analytics summary
app.get('/api/analytics/summary', async (req, res) => {
  try {
    // Analytics logging disabled - return stub data
    res.json({
      success: true,
      data: {
        searches_last_24h: 0,
        recent_searches: []
      }
    });
  } catch (error) {
    console.error('Error fetching analytics:', error.message);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch analytics'
    });
  }
});

// ============================================================
// ERROR HANDLING
// ============================================================

app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: 'Route not found'
  });
});

app.use((err, req, res, next) => {
  console.error('Server error:', err);
  res.status(500).json({
    success: false,
    error: 'Internal server error'
  });
});

// ============================================================
// START SERVER
// ============================================================

app.listen(PORT, () => {
  console.log(`Node API Service running on port ${PORT}`);
  console.log(`Python ML Service URL: ${PYTHON_SERVICE_URL}`);
});

module.exports = app;
