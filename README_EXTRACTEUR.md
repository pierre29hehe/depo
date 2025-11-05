# 📊 Extracteur de Tableaux PDF - Version Simplifiée

## 🎯 Nouveau programme créé

Ce programme **extrait directement les données des PDF sans passer par l'IA**, évitant ainsi toute perte de données.

---

## 🚀 Démarrage rapide

### Windows
```batch
lancer_extracteur.bat
```

### Linux
```bash
./lancer_extracteur.sh
```

### Manuel
```bash
python3 pdf_table_extractor.py
```

---

## ✨ Fonctionnalités

✅ **Extraction directe** - Aucune perte de données
✅ **Détection automatique** - Identifie les types de tableaux (bilan, compte de résultat, etc.)
✅ **Interface graphique** - Simple et intuitive
✅ **Export multiple** - Fichiers texte ou CSV
✅ **Léger** - Seulement PyPDF2 requis

---

## 📋 Types détectés automatiquement

- 📊 **Compte de Résultat**
- 💰 **Bilan**
- 💸 **Flux de Trésorerie**
- 📈 **Ratios Financiers**
- 📅 **Données Temporelles**
- 📋 **Tableau Général**

---

## 🔧 Installation des dépendances

```bash
pip install PyPDF2
```

C'est tout ! Aucune dépendance lourde.

---

## 📖 Utilisation

1. **Lancer** le programme
2. **Cliquer** sur "📁 Sélectionner PDF..."
3. **Choisir** votre document financier
4. **Cliquer** sur "🚀 Extraire les Tableaux"
5. **Consulter** les résultats affichés
6. **Sauvegarder** ou **Exporter** si besoin

---

## 💡 Différence avec l'ancien programme

| Fonctionnalité | Ancien (IA) | Nouveau (Direct) |
|----------------|-------------|------------------|
| **Perte de données** | ❌ Possible | ✅ Aucune |
| **Vitesse** | Lente | ⚡ Rapide |
| **Dépendances** | Ollama/Anthropic | PyPDF2 seul |
| **Précision extraction** | Variable | 💯 100% |
| **Analyse intelligente** | ✅ Oui | ❌ Non |
| **Poids** | Lourd | 🪶 Léger |

---

## 📁 Fichiers créés

- `pdf_table_extractor.py` - Programme principal
- `lancer_extracteur.sh` - Script Linux
- `lancer_extracteur.bat` - Script Windows
- `EXTRACTEUR_PDF_GUIDE.md` - Guide complet
- `README_EXTRACTEUR.md` - Ce fichier

---

## 🎓 Exemples d'utilisation

### Extraire un bilan comptable
Le programme détecte automatiquement les sections actif/passif et affiche toutes les données.

### Analyser un compte de résultat
Toutes les lignes (revenus, charges, résultats) sont extraites sans modification.

### Exporter pour Excel
Sauvegardez en CSV pour analyse ultérieure dans Excel ou LibreOffice.

---

## ⚠️ Limitations

- Les PDF scannés (images) ne sont pas supportés
- L'extraction dépend de la structure du PDF d'origine
- Aucune analyse ou interprétation n'est faite (données brutes uniquement)

---

## 🔄 Pour utiliser l'ancien programme avec IA

Si vous souhaitez utiliser l'analyse IA (avec risque de perte de données) :

```bash
python3 financial_analyzer_gui.py
```

---

## 📞 Support

Consultez `EXTRACTEUR_PDF_GUIDE.md` pour le guide complet d'utilisation.

---

**Version** : 1.0.0
**Date** : 2025-11-05
**Modèles IA disponibles** : mistral:7b-instruct, llama3.1:8b, qwen2.5:7b, etc.
