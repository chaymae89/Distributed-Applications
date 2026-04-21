print("=== TP 6.3 - Sécurité API ===")

security_cases = [
    {
        "surface": "Endpoint login",
        "threat": "Brute force",
        "control": "Rate limiting"
    },
    {
        "surface": "Token",
        "threat": "Token volé",
        "control": "Expiration + HTTPS"
    },
    {
        "surface": "Données JSON",
        "threat": "Injection",
        "control": "Validation des entrées"
    },
    {
        "surface": "ID documents",
        "threat": "Enumeration",
        "control": "UUID v4"
    },
    {
        "surface": "API",
        "threat": "Accès non autorisé",
        "control": "Auth + rôles"
    }
]

for s in security_cases:
    print(f"\nSurface : {s['surface']}")
    print(f"Menace : {s['threat']}")
    print(f"Contrôle : {s['control']}")