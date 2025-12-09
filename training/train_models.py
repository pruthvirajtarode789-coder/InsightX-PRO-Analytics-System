# training/train_models.py
import pandas as pd, joblib, os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

BASE = os.path.dirname(__file__)
data_path = os.path.join(BASE, "..", "data", "customers_sample.csv")
out_dir = os.path.join(BASE, "..", "models")
os.makedirs(out_dir, exist_ok=True)

print("Loading customers data...")
df = pd.read_csv(data_path)
X = df[["total_orders","avg_order_value","tenure_days"]].fillna(0.0)
scaler = StandardScaler()
Xs = scaler.fit_transform(X)
km = KMeans(n_clusters=4, random_state=42).fit(Xs)
joblib.dump({"scaler":scaler, "kmeans":km}, os.path.join(out_dir, "segmentation.joblib"))
print("Saved segmentation model to models/segmentation.joblib")
