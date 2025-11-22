import pandas as pd

# Read just the headers
merchants_df = pd.read_csv('merchant_synthetic_100k_phase6.csv', nrows=0)
edges_df = pd.read_csv('merchant_edges.csv', nrows=0)

print("=== MERCHANTS CSV COLUMNS ===")
for i, col in enumerate(merchants_df.columns):
    print(f"{i}: {col}")

print("\n=== EDGES CSV COLUMNS ===")
for i, col in enumerate(edges_df.columns):
    print(f"{i}: {col}")
