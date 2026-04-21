import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# CONSTANTES DE SÉCURITÉ
# ──────────────────────────────────────────────
MAX_XML_SIZE = 1_000_000  # 1 Mo maximum
EXPECTED_FIELDS = {"id", "title", "author", "date"}


def parse_document_xml(raw_xml: str) -> dict:
    """Parse un XML de métadonnées document de manière défensive."""

    # Contrôle 1 : taille maximale AVANT tout parsing
    if len(raw_xml) > MAX_XML_SIZE:
        logger.warning("XML trop volumineux : %d octets", len(raw_xml))
        raise ValueError("Payload trop volumineux")

    # Contrôle 2 : rejet basique de DOCTYPE (défense en profondeur)
    if " in raw_xml.upper() or " in raw_xml.upper():
        logger.warning("DOCTYPE/ENTITY détecté dans XML — rejeté")
        raise ValueError("Payload invalide")

    # Contrôle 3 : parsing
    try:
        root = ET.fromstring(raw_xml)
    except ET.ParseError as e:
        logger.warning("XML mal formé : %s", e)
        raise ValueError("Payload invalide")

    # Contrôle 4 : extraire uniquement les champs attendus
    result = {}
    for field_name in EXPECTED_FIELDS:
        elem = root.find(field_name)
        if elem is not None and elem.text:
            result[field_name] = elem.text.strip()

    # Contrôle 5 : champs obligatoires
    missing = {"id", "title"} - result.keys()
    if missing:
        logger.warning("Champs manquants dans XML : %s", missing)
        raise ValueError("Payload invalide")

    return result


# ──────────────────────────────────────────────
# TEST
# ──────────────────────────────────────────────
if __name__ == "__main__":
    xml_input = """<?xml version="1.0" encoding="UTF-8"?>
    <document>
        <id>42</id>
        <title>Rapport annuel</title>
        <author>Bob</author>
        <date>2026-01-15</date>
    </document>"""

    result = parse_document_xml(xml_input)
    print("Parsé :", result)