import pickle

print("===== TEST TP7.4 =====")

data = {"id": 1, "name": "Alice"}

# Sérialisation
serialized = pickle.dumps(data)
print("Données sérialisées (pickle) :", serialized)

# Désérialisation
deserialized = pickle.loads(serialized)
print("Données désérialisées :", deserialized)