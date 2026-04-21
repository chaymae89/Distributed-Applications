import json

# =========================
# Lecteur V1
# =========================
def read_document_v1(raw: str) -> dict:
    data = json.loads(raw)

    # Vérifications minimales
    if not isinstance(data["id"], int):
        raise ValueError("Champ 'id' invalide pour V1")
    if not isinstance(data["title"], str):
        raise ValueError("Champ 'title' invalide pour V1")
    if not isinstance(data["author"], str):
        raise ValueError("Champ 'author' invalide pour V1")

    # V1 ignore les champs inconnus
    return {
        "id": data["id"],
        "title": data["title"],
        "author": data["author"]
    }

# =========================
# Lecteur V2
# =========================
def read_document_v2(raw: str) -> dict:
    data = json.loads(raw)

    # Vérifications minimales
    if not isinstance(data["id"], int):
        raise ValueError("Champ 'id' invalide pour V2")
    if not isinstance(data["title"], str):
        raise ValueError("Champ 'title' invalide pour V2")
    if not isinstance(data["author"], str):
        raise ValueError("Champ 'author' invalide pour V2")

    tags = data.get("tags", [])
    classification = data.get("classification", "internal")

    if not isinstance(tags, list):
        raise ValueError("Champ 'tags' invalide pour V2")
    if not isinstance(classification, str):
        raise ValueError("Champ 'classification' invalide pour V2")

    return {
        "id": data["id"],
        "title": data["title"],
        "author": data["author"],
        "tags": tags,
        "classification": classification
    }

# =========================
# Payloads de test
# =========================
doc_v1 = json.dumps({
    "id": 1,
    "title": "Rapport V1",
    "author": "Alice"
}, ensure_ascii=False)

doc_v2 = json.dumps({
    "id": 2,
    "title": "Rapport V2",
    "author": "Bob",
    "tags": ["finance", "audit"],
    "classification": "confidential"
}, ensure_ascii=False)

doc_broken = json.dumps({
    "id": "deux",
    "title": "Rapport cassé",
    "author": "Charlie"
}, ensure_ascii=False)

# =========================
# Tests de compatibilité
# =========================
if __name__ == "__main__":
    print("===== TESTS TP7.2 =====")

    # 1) v1 lit v1
    try:
        result = read_document_v1(doc_v1)
        print("v1 lit v1 : OK ->", result)
    except Exception as e:
        print("v1 lit v1 : ECHEC ->", e)

    # 2) v2 lit v1
    try:
        result = read_document_v2(doc_v1)
        print("v2 lit v1 : OK ->", result)
    except Exception as e:
        print("v2 lit v1 : ECHEC ->", e)

    # 3) v1 lit v2
    try:
        result = read_document_v1(doc_v2)
        print("v1 lit v2 : OK ->", result)
    except Exception as e:
        print("v1 lit v2 : ECHEC ->", e)

    # 4) v2 lit v2
    try:
        result = read_document_v2(doc_v2)
        print("v2 lit v2 : OK ->", result)
    except Exception as e:
        print("v2 lit v2 : ECHEC ->", e)

    # 5) cassure par changement de type
    try:
        result = read_document_v1(doc_broken)
        print("v1 lit document cassé : OK ->", result)
    except Exception as e:
        print("v1 lit document cassé : ECHEC ->", e)

    # 6) même cassure vue par v2
    try:
        result = read_document_v2(doc_broken)
        print("v2 lit document cassé : OK ->", result)
    except Exception as e:
        print("v2 lit document cassé : ECHEC ->", e)