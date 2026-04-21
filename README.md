# 📚 Travaux Pratiques - Systèmes Distribués

## 📖 Description
Ce repository regroupe l’ensemble des travaux pratiques réalisés durant le semestre dans le module **Systèmes Distribués**.

Les TP portent principalement sur :
- Communication client/serveur
- API 
- Gestion des erreurs (retry)
- Programmation asynchrone
- Sérialisation des données (JSON, Pickle, Protobuf)

---

## 📂 Structure du projet

### 🔹 api_project/
Implémentation d'une API client/serveur :
- `server_api.py` : serveur
- `client_api.py` : client
- `retry_example.py` : gestion des retries

---

### 🔹 distributed_tp/
Travaux pratiques sur la communication distribuée :
- `serveur.py` : serveur
- `client.py` : client
- `async_example.py` : communication asynchrone
- `retry_client.py` : gestion des erreurs et retry

---

### 🔹 séance6_distributed/
TP de la séance 6 :
- `server_api.py` : serveur API
- `client_api.py` : client API
- `client_retry.py` : retry avancé

---

### 🔹 tp_séance7/
TP sur la sérialisation des données :

#### 📁 demo_serialisation/
- `tp71_json_validation.py` : validation JSON
- `tp72_versioning_json.py` : versioning JSON
- `tp73_protobuf.py` : introduction à Protocol Buffers
- `tp74_pickle_demo.py` : sérialisation avec Pickle

#### 📄 Autres fichiers
- `document.proto` : définition des structures Protobuf
- `document_pb2.py` : code généré automatiquement

---

## ⚙️ Technologies utilisées
- Python
- HTTP
- JSON
- Protocol Buffers
- Pickle

---

## 🎯 Objectifs pédagogiques
- Comprendre la communication entre client et serveur
- Gérer les erreurs réseau (retry)
- Implémenter des appels simples entre services
- Manipuler différents formats de sérialisation
- Introduire les bases des systèmes distribués

---

## 🚀 Exécution

Exemple pour lancer un serveur :
```bash
python server_api.py
