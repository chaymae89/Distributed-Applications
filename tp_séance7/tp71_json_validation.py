import json
import logging
import re
from dataclasses import dataclass, field, asdict
from typing import List

logging.basicConfig(level=logging.WARNING, format="%(message)s")
logger = logging.getLogger(__name__)

# =========================
# Constantes de validation
# =========================
ALLOWED_CLASSIFICATIONS = {"public", "internal", "confidential", "secret"}
ALLOWED_ROLES = {"viewer", "editor", "admin"}

MAX_TITLE_LEN = 200
MAX_AUTHOR_LEN = 100
MAX_TAGS = 20
MAX_TAG_LEN = 50
MAX_DISPLAY_NAME_LEN = 100

USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]{3,30}$")

# =========================
# Dataclasses
# =========================
@dataclass
class Document:
    id: int
    title: str
    author: str
    tags: List[str] = field(default_factory=list)
    classification: str = "internal"
    created_at: str = ""
    _internal_score: float = field(default=0.0, repr=False)

@dataclass
class UserPublic:
    username: str
    display_name: str
    role: str

# =========================
# Sérialisation
# =========================
def serialize_document(doc: Document) -> str:
    data = {k: v for k, v in asdict(doc).items() if not k.startswith("_")}
    return json.dumps(data, ensure_ascii=False)

def serialize_user_public(user: UserPublic) -> str:
    data = asdict(user)
    return json.dumps(data, ensure_ascii=False)

# =========================
# Désérialisation + validation Document
# =========================
def deserialize_document(raw: str) -> Document:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        logger.warning("JSON invalide : %s", e)
        raise ValueError("Payload invalide")

    if not isinstance(data, dict):
        raise ValueError("Payload invalide")

    errors = []

    # Champs obligatoires
    for f in ("id", "title", "author"):
        if f not in data:
            errors.append(f"Champ obligatoire manquant : {f}")

    # id
    if "id" in data:
        if not isinstance(data["id"], int):
            errors.append("'id' doit être un entier")
        elif data["id"] <= 0:
            errors.append("'id' doit être > 0")

    # title
    if "title" in data:
        if not isinstance(data["title"], str):
            errors.append("'title' doit être une chaîne")
        else:
            title = data["title"].strip()
            if len(title) == 0:
                errors.append("'title' ne peut pas être vide")
            elif len(title) > MAX_TITLE_LEN:
                errors.append("Titre trop long")

    # author
    if "author" in data:
        if not isinstance(data["author"], str):
            errors.append("'author' doit être une chaîne")
        else:
            author = data["author"].strip()
            if len(author) == 0:
                errors.append("'author' ne peut pas être vide")
            elif len(author) > MAX_AUTHOR_LEN:
                errors.append("Auteur trop long")

    # tags
    tags = data.get("tags", [])
    if not isinstance(tags, list):
        errors.append("'tags' doit être une liste")
    elif len(tags) > MAX_TAGS:
        errors.append("Trop de tags")
    else:
        for t in tags:
            if not isinstance(t, str):
                errors.append("Chaque tag doit être une chaîne")
                break
            if len(t.strip()) == 0 or len(t.strip()) > MAX_TAG_LEN:
                errors.append("Tag invalide")
                break

    # classification
    classification = data.get("classification", "internal")
    if not isinstance(classification, str):
        errors.append("'classification' doit être une chaîne")
    elif classification not in ALLOWED_CLASSIFICATIONS:
        errors.append("Classification non autorisée")

    # created_at optionnel
    created_at = data.get("created_at", "")
    if created_at != "" and not isinstance(created_at, str):
        errors.append("'created_at' doit être une chaîne")

    if errors:
        logger.warning("Validation échouée : %s", errors)
        raise ValueError("Payload invalide")

    return Document(
        id=data["id"],
        title=data["title"].strip(),
        author=data["author"].strip(),
        tags=[t.strip() for t in tags],
        classification=classification,
        created_at=created_at.strip() if isinstance(created_at, str) else ""
    )

# =========================
# Désérialisation + validation UserPublic
# =========================
def deserialize_user_public(raw: str) -> UserPublic:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        logger.warning("JSON invalide : %s", e)
        raise ValueError("Payload invalide")

    if not isinstance(data, dict):
        raise ValueError("Payload invalide")

    errors = []

    for f in ("username", "display_name", "role"):
        if f not in data:
            errors.append(f"Champ obligatoire manquant : {f}")

    if "username" in data:
        if not isinstance(data["username"], str):
            errors.append("'username' doit être une chaîne")
        elif not USERNAME_PATTERN.match(data["username"]):
            errors.append("'username' invalide")

    if "display_name" in data:
        if not isinstance(data["display_name"], str):
            errors.append("'display_name' doit être une chaîne")
        else:
            display_name = data["display_name"].strip()
            if len(display_name) == 0:
                errors.append("'display_name' ne peut pas être vide")
            elif len(display_name) > MAX_DISPLAY_NAME_LEN:
                errors.append("'display_name' trop long")

    if "role" in data:
        if not isinstance(data["role"], str):
            errors.append("'role' doit être une chaîne")
        elif data["role"] not in ALLOWED_ROLES:
            errors.append("Rôle non autorisé")

    if errors:
        logger.warning("Validation UserPublic échouée : %s", errors)
        raise ValueError("Payload invalide")

    return UserPublic(
        username=data["username"].strip(),
        display_name=data["display_name"].strip(),
        role=data["role"]
    )

# =========================
# Tests
# =========================
if __name__ == "__main__":
    print("===== TESTS TP7.1 =====")

    # Test valide 1 : Document
    doc = Document(
        id=1,
        title="Rapport Q1",
        author="Alice Dupont",
        tags=["finance", "audit"],
        classification="internal",
        created_at="2026-01-15T10:30:00Z",
        _internal_score=9.5
    )
    json_doc = serialize_document(doc)
    print("Document sérialisé :", json_doc)
    print("Document désérialisé :", deserialize_document(json_doc))

    # Test valide 2 : UserPublic
    user_json = '{"username":"alice_d","display_name":"Alice Dupont","role":"editor"}'
    print("UserPublic désérialisé :", deserialize_user_public(user_json))

    # Test invalide 1 : champ manquant
    try:
        deserialize_document('{"id": 5, "title": "Sans auteur"}')
    except ValueError as e:
        print("Document rejeté 1 :", e)

    # Test invalide 2 : type erroné
    try:
        deserialize_document('{"id": "abc", "title": "Rapport", "author": "Alice"}')
    except ValueError as e:
        print("Document rejeté 2 :", e)

    # Test invalide 3 : valeur hors allowlist
    try:
        deserialize_user_public('{"username":"admin_1","display_name":"Admin Test","role":"superadmin"}')
    except ValueError as e:
        print("UserPublic rejeté 3 :", e)