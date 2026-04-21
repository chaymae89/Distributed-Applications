import json
from dataclasses import dataclass, field, asdict
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# MODÈLE : Document (via dataclass)
# ──────────────────────────────────────────────
@dataclass
class Document:
    id: int
    title: str
    author: str
    tags: List[str] = field(default_factory=list)
    classification: str = "internal"
    # Champ sensible : ne sera PAS sérialisé
    _internal_score: float = field(default=0.0, repr=False)


# ──────────────────────────────────────────────
# SÉRIALISATION : exclure les champs sensibles
# ──────────────────────────────────────────────
EXCLUDED_FIELDS = {"_internal_score"}

def serialize_document(doc: Document) -> str:
    """Sérialise un Document en JSON, sans champs sensibles."""
    data = {k: v for k, v in asdict(doc).items()
            if k not in EXCLUDED_FIELDS}
    return json.dumps(data, ensure_ascii=False)


# ──────────────────────────────────────────────
# VALIDATION + DÉSÉRIALISATION
# ──────────────────────────────────────────────
ALLOWED_CLASSIFICATIONS = {"public", "internal", "confidential", "secret"}
MAX_TITLE_LEN = 200
MAX_TAGS = 20

def deserialize_document(raw: str) -> Document:
    """Désérialise et valide un JSON en Document."""
    # Étape 1 : parsing JSON
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        logger.warning("JSON invalide : %s", e)
        raise ValueError("Payload invalide")

    # Étape 2 : doit être un dict
    if not isinstance(data, dict):
        raise ValueError("Payload invalide")

    errors = []

    # Étape 3 : champs obligatoires
    for f in ("id", "title", "author"):
        if f not in data:
            errors.append(f"Champ obligatoire manquant : {f}")

    # Étape 4 : vérification de types
    if "id" in data and not isinstance(data["id"], int):
        errors.append("'id' doit être un entier")

    if "title" in data:
        if not isinstance(data["title"], str):
            errors.append("'title' doit être une chaîne")
        elif len(data["title"]) > MAX_TITLE_LEN:
            errors.append("Titre trop long")

    if "author" in data and not isinstance(data["author"], str):
        errors.append("'author' doit être une chaîne")

    # Étape 5 : tags (optionnel, liste de strings)
    tags = data.get("tags", [])
    if not isinstance(tags, list):
        errors.append("'tags' doit être une liste")
    elif len(tags) > MAX_TAGS:
        errors.append("Trop de tags")
    elif not all(isinstance(t, str) for t in tags):
        errors.append("Chaque tag doit être une chaîne")

    # Étape 6 : classification (optionnel, allowlist)
    classification = data.get("classification", "internal")
    if classification not in ALLOWED_CLASSIFICATIONS:
        errors.append("Classification non autorisée")

    # Étape 7 : fail closed
    if errors:
        logger.warning("Validation échouée : %s", errors)
        raise ValueError("Payload invalide")  # Message générique côté client

    return Document(
        id=data["id"],
        title=data["title"].strip(),
        author=data["author"].strip(),
        tags=tags,
        classification=classification,
    )


# ──────────────────────────────────────────────
# TEST
# ──────────────────────────────────────────────
if __name__ == "__main__":
    doc = Document(id=1, title="Rapport Q1", author="Alice",
                    tags=["finance"], _internal_score=9.5)

    # Sérialisation (sans le champ sensible)
    json_out = serialize_document(doc)
    print("Sérialisé :", json_out)

    # Désérialisation + validation
    doc2 = deserialize_document(json_out)
    print("Désérialisé :", doc2)

    # Test invalide
    try:
        deserialize_document('{"id": "abc", "title": 123}')
    except ValueError as e:
        print("Rejeté :", e)  # "Payload invalide"