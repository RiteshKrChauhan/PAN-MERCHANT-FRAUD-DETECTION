from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env'))

app = Flask(__name__)
CORS(app)

# Global variables to store data
merchants_df = None
graph = None
embeddings_matrix = None
merchant_id_to_idx = {}
fraud_rings = {}

# Database connection parameters
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'fraud_detection'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

# City mapping for India
CITY_MAPPING = {
    'City_1': 'Mumbai', 'City_2': 'Delhi', 'City_3': 'Bangalore', 
    'City_4': 'Hyderabad', 'City_5': 'Chennai', 'City_6': 'Kolkata',
    'City_7': 'Pune', 'City_8': 'Ahmedabad', 'City_9': 'Surat',
    'City_10': 'Jaipur', 'City_11': 'Lucknow', 'City_12': 'Kanpur',
    'City_13': 'Nagpur', 'City_14': 'Indore', 'City_15': 'Thane',
    'City_16': 'Bhopal', 'City_17': 'Visakhapatnam', 'City_18': 'Pimpri-Chinchwad',
    'City_19': 'Patna', 'City_20': 'Vadodara', 'City_21': 'Ghaziabad',
    'City_22': 'Ludhiana', 'City_23': 'Agra', 'City_24': 'Nashik',
    'City_25': 'Faridabad', 'City_26': 'Meerut', 'City_27': 'Rajkot',
    'City_28': 'Kalyan-Dombivali', 'City_29': 'Vasai-Virar', 'City_30': 'Varanasi',
    'City_31': 'Srinagar', 'City_32': 'Aurangabad', 'City_33': 'Dhanbad',
    'City_34': 'Amritsar', 'City_35': 'Navi Mumbai', 'City_36': 'Allahabad',
    'City_37': 'Ranchi', 'City_38': 'Howrah', 'City_39': 'Coimbatore',
    'City_40': 'Jabalpur', 'City_41': 'Gwalior', 'City_42': 'Vijayawada',
    'City_43': 'Jodhpur', 'City_44': 'Madurai', 'City_45': 'Raipur',
    'City_46': 'Kota', 'City_47': 'Chandigarh', 'City_48': 'Guwahati',
    'City_49': 'Solapur', 'City_50': 'Hubli-Dharwad',
    'City_51': 'Bareilly', 'City_52': 'Moradabad', 'City_53': 'Mysore', 
    'City_54': 'Tiruchirappalli', 'City_55': 'Tiruppur', 'City_56': 'Gurgaon',
    'City_57': 'Aligarh', 'City_58': 'Jalandhar', 'City_59': 'Bhubaneswar',
    'City_60': 'Salem', 'City_61': 'Warangal', 'City_62': 'Mira-Bhayandar',
    'City_63': 'Thiruvananthapuram', 'City_64': 'Bhiwandi', 'City_65': 'Saharanpur',
    'City_66': 'Gorakhpur', 'City_67': 'Guntur', 'City_68': 'Bikaner',
    'City_69': 'Amravati', 'City_70': 'Noida', 'City_71': 'Jamshedpur',
    'City_72': 'Bhilai', 'City_73': 'Cuttack', 'City_74': 'Firozabad',
    'City_75': 'Vellore', 'City_76': 'Udaipur', 'City_77': 'Jhansi',
    'City_78': 'Ulhasnagar', 'City_79': 'Siliguri', 'City_80': 'Dewas',
    'City_81': 'Kurnool', 'City_82': 'Tumkur', 'City_83': 'Rohtak',
    'City_84': 'Panipat', 'City_85': 'Darbhanga', 'City_86': 'Kozhikode',
    'City_87': 'Akola', 'City_88': 'Belgaum', 'City_89': 'Kolhapur',
    'City_90': 'Nanded', 'City_91': 'Ajmer', 'City_92': 'Gaya',
    'City_93': 'Ujjain', 'City_94': 'Loni', 'City_95': 'Sagar',
    'City_96': 'Rourkela', 'City_97': 'Anantapur', 'City_98': 'Bareja',
    'City_99': 'Pondicherry', 'City_100': 'Bhavnagar',
    'City_101': 'Haridwar', 'City_102': 'Nellore', 'City_103': 'Jammu',
    'City_104': 'Muzaffarnagar', 'City_105': 'Malegaon', 'City_106': 'Bathinda',
    'City_107': 'Tirupati', 'City_108': 'Hapur', 'City_109': 'Kakinada',
    'City_110': 'Sirsa', 'City_111': 'Rewa', 'City_112': 'Satna',
    'City_113': 'Ambala', 'City_114': 'Durgapur', 'City_115': 'Shimoga',
    'City_116': 'Ratlam', 'City_117': 'Bardhaman', 'City_118': 'Bijapur',
    'City_119': 'Sonipat', 'City_120': 'Unnao', 'City_121': 'Dehradun',
    'City_122': 'Haldwani', 'City_123': 'Mirzapur', 'City_124': 'Bettiah',
    'City_125': 'Motihari', 'City_126': 'Purnea', 'City_127': 'Jalgaon',
    'City_128': 'Sangli', 'City_129': 'Chittoor', 'City_130': 'Ongole',
    'City_131': 'Nizamabad', 'City_132': 'Karimnagar', 'City_133': 'Palakkad',
    'City_134': 'Kollam', 'City_135': 'Mangalore', 'City_136': 'Bhagalpur',
    'City_137': 'Hajipur', 'City_138': 'Muzaffarpur', 'City_139': 'Beed',
    'City_140': 'Porbandar', 'City_141': 'Jalna', 'City_142': 'Chinsurah',
    'City_143': 'Berhampur', 'City_144': 'Shillong', 'City_145': 'Aizawl',
    'City_146': 'Imphal', 'City_147': 'Kohima', 'City_148': 'Agartala',
    'City_149': 'Srinagar (Uttarakhand)', 'City_150': 'Itanagar',
    'City_151': 'Etawah', 'City_152': 'Bulandshahr', 'City_153': 'Budaun',
    'City_154': 'Alwar', 'City_155': 'Hoshiarpur', 'City_156': 'Maheshtala',
    'City_157': 'Serampore', 'City_158': 'Kharagpur', 'City_159': 'Dibrugarh',
    'City_160': 'Korba', 'City_161': 'Bilaspur', 'City_162': 'Gandhidham',
    'City_163': 'Hingoli', 'City_164': 'Sambalpur', 'City_165': 'Shahjahanpur',
    'City_166': 'Kota (Karnataka)', 'City_167': 'Rewari', 'City_168': 'Vidisha',
    'City_169': 'Katni', 'City_170': 'Morbi', 'City_171': 'Surendranagar',
    'City_172': 'Navsari', 'City_173': 'Gondia', 'City_174': 'Harda',
    'City_175': 'Chhindwara', 'City_176': 'Damoh', 'City_177': 'Mandsaur',
    'City_178': 'Neemuch', 'City_179': 'Sehore', 'City_180': 'Pali',
    'City_181': 'Fatehpur', 'City_182': 'Raiganj', 'City_183': 'Jhunjhunu',
    'City_184': 'Bharatpur', 'City_185': 'Sikar', 'City_186': 'Ganganagar',
    'City_187': 'Banswara', 'City_188': 'Pratapgarh', 'City_189': 'Dausa',
    'City_190': 'Barmer', 'City_191': 'Jalore', 'City_192': 'Churu',
    'City_193': 'Nagaur', 'City_194': 'Koraput', 'City_195': 'Karaikal',
    'City_196': 'Silchar', 'City_197': 'Tezpur', 'City_198': 'Nagaon',
    'City_199': 'Balasore', 'City_200': 'Kendrapara'
}


def get_db_connection():
    """Create database connection"""
    return psycopg2.connect(**DB_CONFIG)


def load_data():
    """Load merchant data from PostgreSQL and build graph"""
    global merchants_df, graph, embeddings_matrix, merchant_id_to_idx, fraud_rings
    
    print("Loading data from PostgreSQL...")
    
    try:
        conn = get_db_connection()
        
        # Load merchant data
        merchants_df = pd.read_sql_query("SELECT * FROM merchants", conn)
        print(f"Loaded {len(merchants_df)} merchants from database")
        
        # Map cities
        merchants_df['city'] = merchants_df['business_city'].map(CITY_MAPPING).fillna(merchants_df['business_city'])
        
        # Extract embedding columns and create matrix for fast similarity calculation
        embedding_cols = [f'emb_{i}' for i in range(16)]
        embeddings_matrix = merchants_df[embedding_cols].values
        merchant_id_to_idx = {mid: idx for idx, mid in enumerate(merchants_df['merchant_id'].values)}
        
        # Load edges and build NetworkX graph
        edges_df = pd.read_sql_query("SELECT * FROM merchant_edges", conn)
        print(f"Loaded {len(edges_df)} edges from database")
        
        conn.close()
        
        # Build NetworkX graph efficiently
        print("Building NetworkX graph...")
        graph = nx.Graph()
        
        # Add all merchants as nodes first
        graph.add_nodes_from(merchants_df['merchant_id'].values)
        
        # Add edges with attributes (use lowercase column names from query)
        edge_list = [(row['merchant_a'], row['merchant_b'], 
                     {'weight': row['weight'], 'reason': row['reason']}) 
                    for _, row in edges_df.iterrows()]
        graph.add_edges_from(edge_list)
        
        print(f"Graph created: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
        
        # Identify fraud rings using NetworkX connected components
        print("Identifying fraud rings using NetworkX connected_components...")
        fraud_merchants = set(merchants_df[merchants_df['is_fraud'] == 1]['merchant_id'].values)
        print(f"Found {len(fraud_merchants)} fraudulent merchants")
        
        # Create subgraph of only fraudulent merchants
        fraud_subgraph = graph.subgraph(fraud_merchants).copy()
        print(f"Fraud subgraph: {fraud_subgraph.number_of_nodes()} nodes, {fraud_subgraph.number_of_edges()} edges")
        
        # Find connected components (fraud rings)
        fraud_rings = {}
        components = list(nx.connected_components(fraud_subgraph))
        print(f"Found {len(components)} connected components")
        
        for idx, component in enumerate(components):
            if len(component) >= 2:  # Only rings with 2+ merchants
                fraud_rings[f"ring_{idx}"] = list(component)
        
        print(f"Identified {len(fraud_rings)} fraud rings with 2+ members")
        
        # Print ring size distribution
        ring_sizes = sorted([len(members) for members in fraud_rings.values()], reverse=True)
        if ring_sizes:
            print(f"Largest ring: {ring_sizes[0]} members")
            print(f"Ring sizes: {ring_sizes[:10]}...")  # Top 10
        
    except Exception as e:
        print(f"Error loading data from database: {e}")
        print("Falling back to CSV files...")
        load_data_from_csv()


def load_data_from_csv():
    """Fallback: Load data from CSV files"""
    global merchants_df, graph, embeddings_matrix, merchant_id_to_idx, fraud_rings
    
    print("Loading data from CSV files...")
    
    # Load merchant data
    merchants_df = pd.read_csv('merchant_synthetic_100k_phase6.csv')
    
    # Map cities
    merchants_df['city'] = merchants_df['business_city'].map(CITY_MAPPING).fillna(merchants_df['business_city'])
    
    # Load edges
    edges_df = pd.read_csv('merchant_edges.csv')
    
    # Extract embeddings
    embedding_cols = [f'emb_{i}' for i in range(16)]
    embeddings_matrix = merchants_df[embedding_cols].values
    merchant_id_to_idx = {mid: idx for idx, mid in enumerate(merchants_df['merchant_id'].values)}
    
    # Build NetworkX graph efficiently
    print("Building NetworkX graph...")
    graph = nx.Graph()
    graph.add_nodes_from(merchants_df['merchant_id'].values)
    
    edge_list = [(row['merchant_A'], row['merchant_B'], 
                 {'weight': row['weight'], 'reason': row['reason']}) 
                for _, row in edges_df.iterrows()]
    graph.add_edges_from(edge_list)
    
    print(f"Graph created: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
    
    # Identify fraud rings using NetworkX
    print("Identifying fraud rings using NetworkX connected_components...")
    fraud_merchants = set(merchants_df[merchants_df['is_fraud'] == 1]['merchant_id'].values)
    print(f"Found {len(fraud_merchants)} fraudulent merchants")
    
    fraud_subgraph = graph.subgraph(fraud_merchants).copy()
    print(f"Fraud subgraph: {fraud_subgraph.number_of_nodes()} nodes, {fraud_subgraph.number_of_edges()} edges")
    
    fraud_rings = {}
    components = list(nx.connected_components(fraud_subgraph))
    print(f"Found {len(components)} connected components")
    
    for idx, component in enumerate(components):
        if len(component) >= 2:
            fraud_rings[f"ring_{idx}"] = list(component)
    
    print(f"Loaded {len(merchants_df)} merchants")
    print(f"Identified {len(fraud_rings)} fraud rings")
    
    # Print ring size distribution
    ring_sizes = sorted([len(members) for members in fraud_rings.values()], reverse=True)
    if ring_sizes:
        print(f"Largest ring: {ring_sizes[0]} members")
        print(f"Ring sizes: {ring_sizes[:10]}...")


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'python-ml-service'})


@app.route('/api/top-fraud-rings', methods=['GET'])
def get_top_fraud_rings():
    """Get top 10 largest fraud rings for visualization"""
    try:
        # Check if data is loaded
        if merchants_df is None or graph is None:
            return jsonify({
                'success': False,
                'error': 'Data not loaded. Please restart the service.'
            }), 500
        
        if not fraud_rings:
            return jsonify({
                'success': False,
                'error': 'No fraud rings found in the dataset.'
            }), 404
        
        # Sort fraud rings by size
        sorted_rings = sorted(fraud_rings.items(), 
                            key=lambda x: len(x[1]), 
                            reverse=True)[:10]
        
        rings_data = []
        for ring_id, members in sorted_rings:
            # Limit visualization for very large rings
            MAX_NODES = 100
            is_truncated = len(members) > MAX_NODES
            display_members = members[:MAX_NODES] if is_truncated else members
            
            ring_data = {
                'ring_id': ring_id,
                'size': len(members),
                'displayed_size': len(display_members),
                'is_truncated': is_truncated,
                'members': display_members,
                'nodes': [],
                'edges': []
            }
            
            # Get member details (limited for large rings)
            for merchant_id in display_members:
                try:
                    merchant = merchants_df[merchants_df['merchant_id'] == merchant_id].iloc[0]
                    ring_data['nodes'].append({
                        'id': merchant_id,
                        'merchant_id': merchant_id,
                        'pan_hash': str(merchant['pan_hash']),
                        'merchant_tier': str(merchant['merchant_tier']),
                        'city': str(merchant.get('city', merchant['business_city'])),
                        'is_fraud': int(merchant['is_fraud'])
                    })
                except Exception as e:
                    print(f"Error getting merchant {merchant_id}: {e}")
                    continue
            
            # Get edges within the ring (limited for large rings)
            try:
                subgraph = graph.subgraph(display_members)
                edge_count = 0
                MAX_EDGES = 200
                
                for u, v, data in subgraph.edges(data=True):
                    if edge_count >= MAX_EDGES:
                        break
                    ring_data['edges'].append({
                        'source': u,
                        'target': v,
                        'weight': float(data.get('weight', 1)),
                        'reason': str(data.get('reason', 'unknown'))
                    })
                    edge_count += 1
                    
            except Exception as e:
                print(f"Error getting edges for ring {ring_id}: {e}")
            
            rings_data.append(ring_data)
        
        return jsonify({
            'success': True,
            'rings': rings_data
        })
    
    except Exception as e:
        print(f"Error in get_top_fraud_rings: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/merchant/<merchant_id>', methods=['GET'])
def get_merchant_info(merchant_id):
    """Get detailed information about a specific merchant"""
    try:
        # Check if merchant exists
        merchant_data = merchants_df[merchants_df['merchant_id'] == merchant_id]
        
        if merchant_data.empty:
            return jsonify({
                'success': False,
                'error': 'Merchant not found'
            }), 404
        
        merchant = merchant_data.iloc[0]
        
        result = {
            'success': True,
            'merchant': {
                'merchant_id': merchant_id,
                'is_fraud': int(merchant['is_fraud']),
                'pan_hash': merchant['pan_hash'],
                'device_id_hash': merchant['device_id_hash'],
                'ip_hash': merchant['ip_hash'],
                'merchant_tier': merchant['merchant_tier'],
                'merchant_category': merchant['merchant_category'],
                'city': merchant['city'],
                'is_kyc_verified': int(merchant['is_kyc_verified']),
                'total_txns_90d': int(merchant['total_txns_90d']),
                'avg_txn_value': float(merchant['avg_txn_value']),
                'chargeback_rate': float(merchant['chargeback_rate']),
                'refund_ratio': float(merchant['refund_ratio']),
                'shared_pan_count': int(merchant['shared_pan_count']),
                'shared_device_count': int(merchant['shared_device_count']),
                'shared_ip_count': int(merchant['shared_ip_count'])
            }
        }
        
        # If merchant is fraud, get network and similar frauds
        if merchant['is_fraud'] == 1:
            # Find the fraud ring this merchant belongs to
            merchant_ring = None
            for ring_id, members in fraud_rings.items():
                if merchant_id in members:
                    merchant_ring = ring_id
                    break
            
            if merchant_ring:
                result['fraud_ring'] = {
                    'ring_id': merchant_ring,
                    'nodes': [],
                    'edges': []
                }
                
                members = fraud_rings[merchant_ring]
                
                # Get nodes
                for mid in members:
                    m = merchants_df[merchants_df['merchant_id'] == mid].iloc[0]
                    result['fraud_ring']['nodes'].append({
                        'id': mid,
                        'merchant_id': mid,
                        'pan_hash': m['pan_hash'],
                        'merchant_tier': m['merchant_tier'],
                        'city': m['city']
                    })
                
                # Get edges
                subgraph = graph.subgraph(members)
                for u, v, data in subgraph.edges(data=True):
                    result['fraud_ring']['edges'].append({
                        'source': u,
                        'target': v,
                        'weight': data.get('weight', 1),
                        'reason': data.get('reason', 'unknown')
                    })
            
            # Get top 10 similar frauds using cosine similarity
            result['similar_frauds'] = get_similar_frauds(merchant_id, top_n=10)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def get_similar_frauds(merchant_id, top_n=10):
    """Calculate top N similar fraud merchants using cosine similarity (optimized)"""
    try:
        # Get index for target merchant
        if merchant_id not in merchant_id_to_idx:
            return []
        
        target_idx = merchant_id_to_idx[merchant_id]
        target_embedding = embeddings_matrix[target_idx:target_idx+1]
        
        # Get all fraud merchants (excluding target)
        fraud_mask = (merchants_df['is_fraud'] == 1) & (merchants_df['merchant_id'] != merchant_id)
        fraud_merchants_df = merchants_df[fraud_mask].copy()
        
        if fraud_merchants_df.empty:
            return []
        
        # Get fraud embeddings efficiently
        fraud_indices = [merchant_id_to_idx[mid] for mid in fraud_merchants_df['merchant_id'].values]
        fraud_embeddings = embeddings_matrix[fraud_indices]
        
        # Calculate cosine similarity (vectorized)
        similarities = cosine_similarity(target_embedding, fraud_embeddings)[0]
        
        # Get top N
        top_indices = np.argsort(similarities)[::-1][:top_n]
        
        similar_frauds = []
        for idx in top_indices:
            fraud_data = fraud_merchants_df.iloc[idx]
            
            similar_frauds.append({
                'merchant_id': fraud_data['merchant_id'],
                'similarity_score': float(similarities[idx]),
                'pan_hash': fraud_data['pan_hash'],
                'merchant_tier': fraud_data['merchant_tier'],
                'city': fraud_data['city'],
                'avg_txn_value': float(fraud_data['avg_txn_value']),
                'chargeback_rate': float(fraud_data['chargeback_rate'])
            })
        
        return similar_frauds
    
    except Exception as e:
        print(f"Error calculating similar frauds: {e}")
        return []


@app.route('/api/search', methods=['POST'])
def search_merchant():
    """Search for merchant by ID"""
    try:
        data = request.get_json()
        merchant_id = data.get('merchant_id', '').strip()
        
        if not merchant_id:
            return jsonify({
                'success': False,
                'error': 'Merchant ID is required'
            }), 400
        
        # Redirect to merchant info endpoint
        return get_merchant_info(merchant_id)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    # Load data on startup
    load_data()
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
