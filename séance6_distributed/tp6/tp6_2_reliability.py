print("=== TP 6.2 - Politiques de Fiabilité ===")

scenarios = [
    {
        "scenario": "Serveur lent",
        "problem": "Temps de réponse élevé",
        "solution": "Timeout (5s)",
    },
    {
        "scenario": "Serveur indisponible",
        "problem": "Connexion refusée",
        "solution": "Retry + backoff exponentiel",
    },
    {
        "scenario": "Erreur 500",
        "problem": "Erreur interne serveur",
        "solution": "Retry limité",
    },
    {
        "scenario": "Trop de requêtes (429)",
        "problem": "Rate limit",
        "solution": "Attendre avant retry",
    },
    {
        "scenario": "Requête non idempotente",
        "problem": "Risque de duplication",
        "solution": "Idempotency-Key",
    }
]

for s in scenarios:
    print(f"\nScénario : {s['scenario']}")
    print(f"Problème : {s['problem']}")
    print(f"Solution : {s['solution']}")