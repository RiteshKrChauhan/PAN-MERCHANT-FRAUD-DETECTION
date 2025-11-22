# 🔍 PAN Merchant Fraud Detection System

A sophisticated fraud detection system that identifies fraudulent merchant networks using graph analytics, machine learning embeddings, and advanced pattern recognition techniques.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Node](https://img.shields.io/badge/node-14+-green.svg)
![React](https://img.shields.io/badge/react-18.2.0-61dafb.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The PAN Merchant Fraud Detection System is an advanced analytical platform designed to detect and visualize fraudulent merchant networks in digital payment ecosystems. By analyzing shared identifiers (PAN, device IDs, IP addresses) and transaction patterns, the system identifies fraud rings and provides actionable insights for risk management teams.

### Key Capabilities

- **Fraud Ring Detection**: Identifies connected networks of fraudulent merchants using graph theory
- **Similarity Analysis**: Uses cosine similarity on merchant embeddings to find related fraud patterns
- **Real-time Visualization**: Interactive graph visualization of fraud networks
- **Merchant Profiling**: Detailed analysis of individual merchant risk indicators
- **Scalable Architecture**: Handles 100,000+ merchants with sub-second query performance

## ✨ Features

### 🔴 Fraud Detection
- **Graph-based Analysis**: NetworkX connected components algorithm for fraud ring detection
- **85+ Fraud Rings**: Identifies complex fraud networks ranging from 2 to 7,699+ members
- **Risk Indicators**: Tracks shared PANs, devices, IPs, and transaction anomalies

### 📊 Advanced Analytics
- **Cosine Similarity**: 16-dimensional embedding space for merchant similarity
- **Transaction Metrics**: Analyzes 90-day patterns, chargeback rates, refund ratios
- **Behavioral Scoring**: KYC verification, merchant tier, category analysis

### 🎨 Interactive Dashboard
- **Dark Blue/Teal Theme**: Modern, professional UI with high contrast
- **Force-Directed Graphs**: Real-time graph visualization with zoom and pan
- **Smart Truncation**: Handles large networks (7,699 nodes → 100 displayed)
- **Merchant Search**: Instant lookup by merchant ID

### 🚀 Performance
- **PostgreSQL Backend**: Fast queries on 100k+ records
- **Optimized Graph Operations**: NumPy matrix operations for embeddings
- **Lazy Loading**: On-demand data fetching for minimal latency

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + Vite)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │  Dashboard   │  │ Merchant     │  │  Fraud Ring     │  │
│  │              │  │ Details      │  │  Visualization  │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
┌────────────────────────┴────────────────────────────────────┐
│              Node.js API Gateway (Express)                  │
│          ┌──────────────────────────────────┐              │
│          │  Routes: /api/dashboard          │              │
│          │         /api/search              │              │
│          │         /api/merchant/:id        │              │
│          └──────────────────────────────────┘              │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP
┌────────────────────────┴────────────────────────────────────┐
│         Python ML Service (Flask + NetworkX)                │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Fraud Ring   │  │  Cosine      │  │  Merchant       │  │
│  │ Detection    │  │  Similarity  │  │  Analysis       │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ SQL
┌────────────────────────┴────────────────────────────────────┐
│                  PostgreSQL Database                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  merchants (100k rows, 50 columns)                   │  │
│  │  merchant_edges (87k rows, 4 columns)                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 💻 Technology Stack

### Frontend
- **React 18.2.0** - UI library
- **Vite 5.0.8** - Build tool and dev server
- **React Router 6.20.1** - Client-side routing
- **react-force-graph-2d 1.25.4** - Graph visualization
- **D3.js 7.8.5** - Data visualization
- **Axios 1.6.2** - HTTP client

### Backend - Python ML Service
- **Flask 3.0.0** - Web framework
- **NetworkX 3.2.1** - Graph analysis
- **pandas 2.1.4** - Data manipulation
- **NumPy 1.24.3** - Numerical computing
- **scikit-learn 1.3.2** - Machine learning utilities
- **psycopg2-binary 2.9.9** - PostgreSQL adapter

### Backend - Node API Service
- **Express 4.18.2** - Web framework
- **pg** - PostgreSQL client
- **Axios 1.6.2** - HTTP client
- **CORS** - Cross-origin support

### Database
- **PostgreSQL 14+** - Primary data store
- Optimized indexes on fraud flags, tiers, cities

### DevOps
- **Git** - Version control
- **npm** - Package management (Node)
- **pip** - Package management (Python)
- **venv** - Python virtual environment

## 🚀 Installation

### Prerequisites

- **Node.js** 14+ and npm
- **Python** 3.8+
- **PostgreSQL** 14+
- **Git**

### Step 1: Clone Repository

```bash
git clone https://github.com/RiteshKrChauhan/PAN-MERCHANT-FRAUD-DETECTION.git
cd PAN-MERCHANT-FRAUD-DETECTION
cd "Snack Overflow"
```

### Step 2: Database Setup

1. **Create Database**:
```bash
psql -U postgres
CREATE DATABASE fraud_detection;
\q
```

2. **Load Schema**:
```bash
psql -U postgres -d fraud_detection -f backend/database/load_merchant_data.sql
```

3. **Import Data** (using pgAdmin or psql):
   - Import `merchant_synthetic_100k_phase6.csv` into `merchants` table
   - Import `merchant_edges.csv` into `merchant_edges` table

### Step 3: Environment Configuration

Create `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env`:
```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fraud_detection
DB_USER=postgres
DB_PASSWORD=your_password_here

# Service URLs
PYTHON_SERVICE_URL=http://localhost:5000
NODE_PORT=3000
```

### Step 4: Backend - Python ML Service

```bash
cd backend/services/python-ml-service

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
source venv/Scripts/activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run service
python app.py
```

The Python service will run on **http://localhost:5000**

### Step 5: Backend - Node API Service

```bash
cd backend/services/node-api-service

# Install dependencies
npm install

# Run service
npm run dev
```

The Node API will run on **http://localhost:3000**

### Step 6: Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will run on **http://localhost:3001**

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | PostgreSQL host | localhost |
| `DB_PORT` | PostgreSQL port | 5432 |
| `DB_NAME` | Database name | fraud_detection |
| `DB_USER` | Database user | postgres |
| `DB_PASSWORD` | Database password | - |
| `PYTHON_SERVICE_URL` | Python ML service URL | http://localhost:5000 |
| `NODE_PORT` | Node API port | 3000 |

### Vite Configuration

Frontend dev server settings in `frontend/vite.config.js`:
- **Port**: 3001
- **Proxy**: `/api` → `http://localhost:3000`

## 📖 Usage

### 1. Access Dashboard

Open **http://localhost:3001** in your browser.

### 2. View Fraud Rings

- Dashboard displays top 10 fraud rings by size
- Click on any ring button to visualize the network
- Hover over nodes to see merchant details
- Click nodes to open detailed merchant profile

### 3. Search Merchants

- Use search bar in header
- Enter merchant ID (e.g., `MID_00001`)
- View detailed profile, fraud indicators, and connections

### 4. Analyze Networks

- Force-directed graph shows merchant connections
- Edge thickness = connection strength
- Red nodes/edges = fraudulent merchants
- Tooltip shows merchant details on hover

## 📡 API Documentation

### Get Top Fraud Rings

```http
GET /api/dashboard/fraud-rings
```

**Response**:
```json
{
  "success": true,
  "rings": [
    {
      "ring_id": 1,
      "size": 7699,
      "nodes": [...],
      "edges": [...],
      "is_truncated": true,
      "displayed_size": 100
    }
  ]
}
```

### Search Merchant

```http
POST /api/search
Content-Type: application/json

{
  "merchant_id": "MID_00001"
}
```

**Response**:
```json
{
  "success": true,
  "merchant_id": "MID_00001",
  "found": true
}
```

### Get Merchant Details

```http
GET /api/merchant/:merchant_id
```

**Response**:
```json
{
  "success": true,
  "merchant": {
    "merchant_id": "MID_00001",
    "is_fraud": 1,
    "pan_hash": "PAN_ABC123",
    "merchant_tier": "high",
    "city": "Mumbai",
    "total_txns_90d": 1500,
    "avg_txn_value": 2500.50,
    "chargeback_rate": 0.05,
    ...
  },
  "fraud_ring": {
    "nodes": [...],
    "edges": [...]
  },
  "similar_frauds": [...]
}
```

## 🗄️ Database Schema

### `merchants` Table (100,000 rows)

| Column | Type | Description |
|--------|------|-------------|
| merchant_id | VARCHAR(20) | Primary key |
| is_fraud | INTEGER | Fraud flag (0/1) |
| pan_hash | VARCHAR(50) | Hashed PAN card |
| device_id_hash | VARCHAR(50) | Hashed device ID |
| ip_hash | VARCHAR(50) | Hashed IP address |
| business_city | VARCHAR(20) | City code |
| merchant_tier | VARCHAR(20) | Tier (low/medium/high) |
| merchant_category | VARCHAR(50) | Business category |
| total_txns_90d | INTEGER | 90-day transaction count |
| avg_txn_value | DECIMAL(10,2) | Average transaction value |
| chargeback_rate | DECIMAL(5,4) | Chargeback percentage |
| refund_ratio | DECIMAL(5,4) | Refund percentage |
| shared_pan_count | INTEGER | PANs shared with others |
| shared_device_count | INTEGER | Devices shared |
| shared_ip_count | INTEGER | IPs shared |
| emb_0 to emb_15 | DECIMAL(10,6) | 16-dim embeddings |

### `merchant_edges` Table (87,055 rows)

| Column | Type | Description |
|--------|------|-------------|
| merchant_A | VARCHAR(20) | Source merchant |
| merchant_B | VARCHAR(20) | Target merchant |
| weight | DECIMAL(5,2) | Connection strength |
| reason | VARCHAR(100) | Connection reason |

## 📁 Project Structure

```
PAN-MERCHANT-FRAUD-DETECTION/
├── Snack Overflow/
│   ├── backend/
│   │   ├── database/
│   │   │   └── load_merchant_data.sql
│   │   └── services/
│   │       ├── python-ml-service/
│   │       │   ├── app.py
│   │       │   ├── requirements.txt
│   │       │   └── venv/
│   │       └── node-api-service/
│   │           ├── server.js
│   │           ├── package.json
│   │           └── node_modules/
│   ├── frontend/
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── Dashboard.jsx
│   │   │   │   ├── FraudRingGraph.jsx
│   │   │   │   ├── MerchantDetails.jsx
│   │   │   │   ├── SearchBar.jsx
│   │   │   │   ├── Header.jsx
│   │   │   │   ├── StatsCard.jsx
│   │   │   │   └── SimilarFraudsList.jsx
│   │   │   ├── App.jsx
│   │   │   └── index.jsx
│   │   ├── index.html
│   │   ├── vite.config.js
│   │   └── package.json
│   ├── .env
│   ├── .env.example
│   ├── .gitignore
│   └── .gitattributes
└── README.md
```

## 🖼️ Screenshots

### Dashboard - Fraud Ring Overview
Dark blue/teal themed dashboard showing top fraud rings with statistics cards highlighting total rings, largest ring size, and fraudulent merchant count.

### Force-Directed Graph Visualization
Interactive network graph displaying merchant connections with red nodes representing fraudulent merchants, edge thickness indicating connection strength, and hover tooltips showing merchant details.

### Merchant Detail Page
Comprehensive merchant profile showing fraud alerts, transaction metrics, shared identifiers, and connected fraud network visualization.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- **Python**: Follow PEP 8
- **JavaScript**: ES6+ with semicolons
- **React**: Functional components with hooks

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Ritesh Kr Chauhan** - [@RiteshKrChauhan](https://github.com/RiteshKrChauhan)

## 🙏 Acknowledgments

- NetworkX for graph analysis algorithms
- React Force Graph for visualization components
- PostgreSQL for robust data storage
- The open-source community

## 📞 Support

For questions or issues, please:
- Open an issue on GitHub
- Contact: [Your Email]

---

**⭐ Star this repository if you find it helpful!**

*Built with ❤️ for fraud detection and prevention*
