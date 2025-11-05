# Analyseur de Rapports Financiers avec IA

Programme Python qui utilise l'intelligence artificielle **locale ou cloud** pour lire et analyser des rapports financiers automatiquement.

## ✨ Nouveautés !

### 🖥️ Interface Graphique Disponible !
**Sélectionnez vos fichiers en quelques clics !** Interface intuitive avec navigation de dossiers.

### 🤖 Modèles IA Locaux
Utilisez vos propres modèles IA avec **Ollama** - **100% gratuit, rapide et privé** !

Plus besoin de clé API ou de connexion internet. Vos données restent sur votre machine.

## 🚀 Fonctionnalités

- 🖥️ **Interface Graphique** : Sélection facile de fichiers avec fenêtre de navigation
- 📟 **Ligne de Commande** : Pour automatisation et scripts

- 📄 **Lecture multi-format** : PDF, Excel (XLSX/XLS), et CSV
- 🤖 **IA Locale ou Cloud** :
  - **Ollama** (local) : Mistral, Llama 3.1, Qwen, DeepSeek, CodeLlama, etc.
  - **Claude AI** (cloud, optionnel)
- 🧮 **Calculs automatiques** : Ratios financiers, marges, croissance, etc.
- 📊 **Rapports détaillés** : Analyse complète avec recommandations
- 💰 **100% Gratuit** : Avec les modèles locaux
- 🔒 **Privé** : Vos données ne quittent jamais votre PC

## 📥 Installation Rapide

### Option 1 : IA Locale (Recommandé - Gratuit !)

```bash
# 1. Installer Ollama (si pas déjà fait)
curl -fsSL https://ollama.com/install.sh | sh

# 2. Lancer Ollama
ollama serve  # Dans un terminal séparé

# 3. Installer les dépendances Python
pip install -r requirements.txt

# 4. C'est prêt ! Vos modèles sont déjà installés
python financial_analyzer.py --list-models
```

### Option 2 : IA Cloud (Anthropic Claude)

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Configurer la clé API
cp config.example.json config.json
# Éditez config.json avec votre clé API Anthropic
```

**👉 [Guide d'installation complet](INSTALLATION_RAPIDE.md)**

## 🎯 Utilisation

### 🖥️ Mode Interface Graphique (Recommandé pour débuter)

**Le plus simple ! Sélectionnez vos fichiers avec une fenêtre de navigation.**

```bash
# Linux / macOS
./lancer_interface.sh

# Ou directement
python3 financial_analyzer_gui.py
```

**Windows :** Double-cliquez sur `lancer_interface.bat`

📖 **[Guide Interface Graphique Complet](INTERFACE_GRAPHIQUE.md)**

**Fonctionnalités de l'interface :**
- 📁 Sélection de fichiers par navigation visuelle
- ⚙️ Configuration intuitive (backend, modèle, calculs)
- 📊 Résultats en temps réel
- 💾 Sauvegarde en un clic

---

### 📟 Mode Ligne de Commande

**Pour automatisation et utilisateurs avancés**

#### Avec vos modèles locaux (par défaut)

```bash
# Analyse simple avec le modèle par défaut
python financial_analyzer.py rapport.pdf

# Choisir un modèle spécifique
python financial_analyzer.py rapport.pdf --model llama3.1:8b
python financial_analyzer.py rapport.pdf --model mistral:7b-instruct
python financial_analyzer.py rapport.pdf --model qwen2.5-coder:7b
```

### Avec Claude AI (cloud - optionnel)

```bash
python financial_analyzer.py rapport.pdf --backend anthropic
```

### Options avancées

```bash
# Calculer uniquement les ratios
python financial_analyzer.py bilan.xlsx --calculations ratios

# Sauvegarder le résultat
python financial_analyzer.py rapport.pdf --output analyse.txt

# Export JSON
python financial_analyzer.py data.csv --format json --output resultat.json

# Lister les modèles disponibles
python financial_analyzer.py --list-models
```

## 📊 Modèles IA Recommandés

Vous avez déjà ces modèles installés ! Voici lesquels utiliser :

| Modèle | Usage | Commande |
|--------|-------|----------|
| **mistral:7b-instruct** | Analyse générale (excellent français) | `--model mistral:7b-instruct` |
| **llama3.1:8b** | Performance maximale | `--model llama3.1:8b` |
| **qwen2.5-coder:7b** | Calculs complexes | `--model qwen2.5-coder:7b` |
| **deepseek-r1:8b** | Raisonnement approfondi | `--model deepseek-r1:8b` |
| **codellama:7b** | Génération de code | `--model codellama:7b` |
| **qwen2.5:7b** | Équilibre vitesse/qualité | `--model qwen2.5:7b` |

## 🧮 Types de Calculs

Le programme analyse et calcule automatiquement :

### Ratios de Liquidité
- Ratio courant (Current Ratio)
- Ratio de liquidité réduite (Quick Ratio)
- Ratio de trésorerie

### Ratios de Rentabilité
- Marge brute, nette, opérationnelle
- Marge EBITDA
- ROE (Return on Equity)
- ROA (Return on Assets)
- ROI (Return on Investment)

### Ratios d'Endettement
- Ratio dette/capitaux propres
- Ratio dette/actifs
- Ratio de couverture des intérêts

### Analyse de Croissance
- Évolution du chiffre d'affaires
- Croissance des bénéfices
- Taux de croissance annuel composé (CAGR)

## 📄 Formats Supportés

- **PDF** : Rapports annuels, états financiers, bilans
- **Excel** (.xlsx, .xls) : Feuilles de calcul, tableaux financiers
- **CSV** : Données tabulaires, exports comptables
- **Texte** : Fichiers .txt avec données financières

## 📚 Documentation

- **[Interface Graphique](INTERFACE_GRAPHIQUE.md)** - 🖥️ Guide de l'interface avec fenêtre de sélection
- **[Installation Rapide](INSTALLATION_RAPIDE.md)** - Guide complet pour démarrer
- **[Guide d'Utilisation CLI](GUIDE_USAGE.md)** - Exemples ligne de commande détaillés
- **[Configuration](config.example.json)** - Options de configuration

## 💡 Exemples

### Analyser un bilan comptable

```bash
python financial_analyzer.py bilan_2024.xlsx \
  --model llama3.1:8b \
  --calculations all \
  --output analyse_bilan.txt
```

### Analyser plusieurs rapports

```bash
#!/bin/bash
for file in rapports/*.pdf; do
    echo "Analyse: $file"
    python financial_analyzer.py "$file" \
      --model mistral:7b-instruct \
      --calculations ratios \
      --output "analyses/$(basename "$file" .pdf).txt"
done
```

### Utiliser en Python

```python
from financial_analyzer import FinancialReportAnalyzer

# Créer l'analyseur avec un modèle local
analyzer = FinancialReportAnalyzer(
    backend="ollama",
    model="llama3.1:8b"
)

# Analyser un rapport
results = analyzer.process_report("rapport.pdf", calculations="all")

if results["success"]:
    print(results["analysis"])
```

## 🔧 Dépannage

### Ollama n'est pas en cours d'exécution
```bash
# Lancez Ollama dans un terminal séparé
ollama serve
```

### Module ollama non trouvé
```bash
pip install ollama
```

### Lister les modèles disponibles
```bash
python financial_analyzer.py --list-models
```

### Télécharger un nouveau modèle
```bash
ollama pull mistral:7b-instruct
```

### Erreur lors de la lecture PDF (Linux)
```bash
sudo apt-get install poppler-utils
```

## 🌟 Avantages des Modèles Locaux

✅ **Gratuit** - Aucun coût d'API
✅ **Privé** - Vos données restent sur votre machine
✅ **Rapide** - Pas de latence réseau
✅ **Hors ligne** - Fonctionne sans internet
✅ **Illimité** - Pas de limite d'utilisation
✅ **Choix** - Plusieurs modèles disponibles

## 🔗 Ressources

- **Ollama** : https://ollama.ai
- **Modèles disponibles** : https://ollama.ai/library
- **Claude AI** (optionnel) : https://console.anthropic.com/

## 📄 Licence

MIT

## 🤝 Support

Pour toute question :
1. Consultez [INSTALLATION_RAPIDE.md](INSTALLATION_RAPIDE.md)
2. Consultez [GUIDE_USAGE.md](GUIDE_USAGE.md)
3. Vérifiez que Ollama est lancé : `ollama serve`
4. Listez vos modèles : `python financial_analyzer.py --list-models`

---

**Fait avec ❤️ pour analyser vos rapports financiers en toute confidentialité**
