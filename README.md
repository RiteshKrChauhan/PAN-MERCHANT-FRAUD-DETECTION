# PAN Merchant Fraud Detection - Full Stack Application

## 🏗️ Architecture Overview

This is a **hybrid microservices architecture** with:
- **Python ML Service** (Flask) - Handles machine learning, graph analysis, and fraud detection
- **Node.js API Gateway** (Express) - Main API gateway and database operations
- **React Frontend** - Interactive visualization and user interface
- **PostgreSQL Database** - Logs, analytics, and metadata storage

---

## 📁 Project Structure

```
PAN Merchant Fraud Detection/
├── backend/
│   ├── services/
│   │   ├── python-ml-service/        # Python Flask ML Service
│   │   │   ├── app.py
│   │   │   └── requirements.txt
│   │   └── node-api-service/         # Node.js API Gateway
│   │       ├── server.js
│   │       ├── package.json
│   │       └── .env.example
│   └── database/
│       └── schema.sql                # PostgreSQL schema
├── frontend/
│   ├── src/
│   │   ├── components/               # React components
│   │   │   ├── Dashboard.js
│   │   │   ├── MerchantDetails.js
│   │   │   ├── FraudRingGraph.js
│   │   │   ├── SimilarFraudsList.js
│   │   │   ├── Header.js
│   │   │   ├── SearchBar.js
│   │   │   └── StatsCard.js
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   ├── public/
│   └── package.json
└── Snack Overflow/
    └── dataset_generation.ipynb       # ML model and data generation
```

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 13+
- npm or yarn

### 1️⃣ Database Setup

```bash
# Create database
createdb fraud_detection
# Or in psql: CREATE DATABASE fraud_detection;
```

**Load Merchant Data:**

Method 1: Using pgAdmin (Recommended)
1. Open pgAdmin and connect to `fraud_detection` database
2. Run the table creation script:
   - Query Tool → Open File → `backend/database/load_merchant_data.sql`
   - Execute the CREATE TABLE statements
3. Import CSV data:
   - Right-click `merchants` table → Import/Export Data
   - Select `Snack Overflow/merchant_synthetic_100k_phase6.csv`
   - Options: Header = Yes, Format = csv
   - Click OK
4. Repeat for `merchant_edges` table:
   - Select `Snack Overflow/merchant_edges.csv`

Method 2: Using psql command line
```bash
# Run table creation
psql -U postgres -d fraud_detection -f "backend/database/load_merchant_data.sql"

# Import data (adjust path as needed)
psql -U postgres -d fraud_detection -c "\copy merchants FROM 'E:/Capstone Projects/PAN Merchant Fraud Detection/Snack Overflow/merchant_synthetic_100k_phase6.csv' WITH (FORMAT csv, HEADER true);"

psql -U postgres -d fraud_detection -c "\copy merchant_edges FROM 'E:/Capstone Projects/PAN Merchant Fraud Detection/Snack Overflow/merchant_edges.csv' WITH (FORMAT csv, HEADER true);"
```

**Optional: Create logging tables**
```bash
# Only if you want API/search logging
psql -U postgres -d fraud_detection -f "backend/database/schema.sql"
```

### 2️⃣ Python ML Service Setup

```bash
cd backend/services/python-ml-service

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows Git Bash
# or: venv\Scripts\activate  # On Windows CMD

# Install dependencies (including PostgreSQL driver)
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your PostgreSQL credentials:
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=fraud_detection
# DB_USER=postgres
# DB_PASSWORD=your_password

# Run the service
python app.py
```

Python service will run on: **http://localhost:5000**

**Note**: If database connection fails, the service will automatically fall back to CSV files.

### 3️⃣ Node.js API Gateway Setup

```bash
cd backend/services/node-api-service

# Install dependencies
npm install

# Create .env file from example
cp .env.example .env

# Edit .env with your database credentials
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=fraud_detection
# DB_USER=postgres
# DB_PASSWORD=your_password
# PYTHON_SERVICE_URL=http://localhost:5000

# Run the service
npm start
# Or for development with auto-reload
npm run dev
```

Node service will run on: **http://localhost:3000**

### 4️⃣ Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will run on: **http://localhost:3001** (or 3000 if Node service uses different port)

---

## 🔌 API Endpoints

### Node.js API Gateway (Port 3000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/dashboard/fraud-rings` | Get top 10 fraud rings |
| POST | `/api/search` | Search merchant by ID |
| GET | `/api/merchant/:merchant_id` | Get merchant details |
| GET | `/api/analytics/summary` | Get analytics summary |

### Python ML Service (Port 5000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/top-fraud-rings` | Get top fraud rings with graph data |
| GET | `/api/merchant/:merchant_id` | Get merchant info + similar frauds |
| POST | `/api/search` | Search merchant |

---

## 🗄️ Database Schema

### Tables:

1. **api_logs** - Logs all API calls
   - `id` (SERIAL PRIMARY KEY)
   - `endpoint` (VARCHAR)
   - `timestamp` (TIMESTAMP)
   - `success` (BOOLEAN)
   - `error_message` (TEXT)

2. **search_logs** - Logs merchant searches
   - `id` (SERIAL PRIMARY KEY)
   - `merchant_id` (VARCHAR)
   - `timestamp` (TIMESTAMP)
   - `found` (BOOLEAN)

3. **fraud_alerts** - Fraud alert tracking (future use)
4. **user_sessions** - Session tracking (future use)
5. **cached_queries** - Query caching (future use)

### Functions:
- `clean_old_logs()` - Remove logs older than 30 days
- `get_search_stats(days_back)` - Get search statistics

---

## 🎨 Features

### Dashboard
- ✅ Top 10 largest fraud rings visualization
- ✅ Interactive network graphs
- ✅ Node hover to see merchant details (ID, PAN, tier, city)
- ✅ Click nodes to navigate to full details
- ✅ Real-time stats cards

### Merchant Search
- ✅ Search by Merchant ID
- ✅ Fraud/Legitimate classification
- ✅ Complete merchant profile
- ✅ Transaction metrics
- ✅ Shared identifier red flags

### Fraud Analysis (for flagged merchants)
- ✅ Fraud ring network visualization
- ✅ Top 10 similar frauds using **Cosine Similarity**
- ✅ Similarity scores and comparison metrics
- ✅ One-click navigation between related merchants

### City Mapping
- ✅ Maps City_1 to City_50 to real Indian cities (Mumbai, Delhi, Bangalore, etc.)
- ✅ Remaining cities keep original format

---

## 🛠️ Technology Stack

### Backend
- **Python**: Flask, pandas, numpy, networkx, scikit-learn
- **Node.js**: Express, axios, pg (PostgreSQL client)

### Frontend
- **React**: React Router, Hooks
- **Visualization**: react-force-graph-2d (D3-based network graphs)
- **Styling**: CSS3, Responsive design

### Database
- **PostgreSQL**: Relational database for logs and analytics

---

## 📊 Data Flow

1. User searches merchant → Node API → Python ML Service
2. Python service analyzes merchant using:
   - Graph-based fraud ring detection
   - Cosine similarity for finding similar frauds
   - Pre-computed embeddings from Node2Vec
3. Results sent back through Node API to Frontend
4. All searches logged to PostgreSQL

---

## 🔐 Security Notes

- No authentication implemented (as per requirements)
- CORS enabled for development
- Input validation on merchant ID
- SQL injection protection via parameterized queries

---

## 📈 Future Enhancements

- [ ] User authentication and authorization
- [ ] Real-time fraud alerts
- [ ] Advanced analytics dashboard
- [ ] Export fraud reports
- [ ] Batch merchant analysis
- [ ] API rate limiting
- [ ] Caching layer (Redis)

---

## 🐛 Troubleshooting

### Python service won't start
- Ensure data files are in the correct directory
- Check Python version (3.8+)
- Verify all dependencies installed

### Node service database errors
- Verify PostgreSQL is running
- Check .env credentials
- Ensure schema.sql was executed

### Frontend can't connect to API
- Check proxy setting in frontend/package.json
- Verify Node service is running on port 3000
- Check browser console for CORS errors

---

## 👥 Development

```bash
# Run all services concurrently (development)
# Terminal 1: Python ML Service
cd backend/services/python-ml-service && python app.py

# Terminal 2: Node API Gateway
cd backend/services/node-api-service && npm run dev

# Terminal 3: React Frontend
cd frontend && npm start
```

---

## 📝 License

This project is part of a capstone project for educational purposes.

---

## 🤝 Contributing

This is a capstone project. For questions or suggestions, please contact the project team.
