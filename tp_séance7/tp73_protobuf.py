import json
import document_pb2

print("===== TESTS TP7.3 =====")

# =========================
# Création objet Protobuf
# =========================
doc = document_pb2.Document()
doc.id = 42
doc.title = "Rapport Q1"
doc.author = "Alice"
doc.tags.append("finance")
doc.tags.append("audit")
doc.classification = "confidential"

# =========================
# Sérialisation binaire
# =========================
binary_data = doc.SerializeToString()

print("Taille Protobuf :", len(binary_data), "octets")

# =========================
# Désérialisation
# =========================
doc2 = document_pb2.Document()
doc2.ParseFromString(binary_data)

print("ID :", doc2.id)
print("Titre :", doc2.title)
print("Author :", doc2.author)
print("Tags :", list(doc2.tags))
print("Classification :", doc2.classification)

# =========================
# Comparaison avec JSON
# =========================
json_data = json.dumps({
    "id": 42,
    "title": "Rapport Q1",
    "author": "Alice",
    "tags": ["finance", "audit"],
    "classification": "confidential"
}).encode("utf-8")

print("Taille JSON :", len(json_data), "octets")

ratio = len(json_data) / len(binary_data)
print(f"Ratio : Protobuf est ~{ratio:.1f}× plus petit")

# =========================
# Compatibilité (lecture partielle)
# =========================
print("\nTest compatibilité (lecture type V1) :")

doc_v1_view = {
    "id": doc2.id,
    "title": doc2.title,
    "author": doc2.author
}

print("Lecture style V1 :", doc_v1_view)