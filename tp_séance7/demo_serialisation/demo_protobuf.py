import document_pb2  # Module généré par protoc

# ── Encode (sérialisation) ──
doc = document_pb2.Document()
doc.id = 42
doc.title = "Rapport Q1"
doc.author = "Alice"
doc.tags.append("finance")
doc.tags.append("interne")
doc.classification = "confidential"

binary_data = doc.SerializeToString()
print(f"Taille Protobuf : {len(binary_data)} octets")

# ── Decode (désérialisation) ──
doc2 = document_pb2.Document()
doc2.ParseFromString(binary_data)
print(f"Titre : {doc2.title}")
print(f"Tags : {list(doc2.tags)}")

# ── Comparaison de taille avec JSON ──
import json
json_data = json.dumps({
    "id": 42, "title": "Rapport Q1", "author": "Alice",
    "tags": ["finance", "interne"], "classification": "confidential"
}).encode("utf-8")
print(f"Taille JSON : {len(json_data)} octets")
print(f"Ratio : Protobuf est ~{len(json_data) / len(binary_data):.1f}× plus petit")