# Installation Rapide - Modèles IA Locaux

Guide d'installation pour utiliser vos modèles IA locaux avec l'analyseur financier.

## 🚀 Installation en 3 étapes

### 1. Installer Ollama (si pas déjà fait)

**Linux / WSL:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**macOS:**
```bash
brew install ollama
```

**Windows:**
Téléchargez depuis https://ollama.ai/download

### 2. Lancer Ollama

```bash
ollama serve
```

(Laissez cette commande tourner dans un terminal)

### 3. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

## 📥 Télécharger vos modèles

Vous avez déjà ces modèles ! Voici comment les utiliser :

```bash
# Si besoin de télécharger
ollama pull mistral:7b-instruct
ollama pull llama3.1:8b
ollama pull qwen2.5-coder:7b
```

## ✅ Vérifier vos modèles

```bash
# Lister tous les modèles installés
ollama list

# Ou avec le programme
python financial_analyzer.py --list-models
```

## 🎯 Utilisation

### Analyse simple (avec le modèle par défaut)

```bash
python financial_analyzer.py votre_rapport.pdf
```

### Choisir un modèle spécifique

```bash
# Avec Mistral (excellent français)
python financial_analyzer.py rapport.pdf --model mistral:7b-instruct

# Avec Llama 3.1 (très performant)
python financial_analyzer.py rapport.pdf --model llama3.1:8b

# Avec Qwen Coder (spécialisé calculs)
python financial_analyzer.py rapport.pdf --model qwen2.5-coder:7b

# Avec DeepSeek (raisonnement complexe)
python financial_analyzer.py rapport.pdf --model deepseek-r1:8b
```

### Sauvegarder le résultat

```bash
python financial_analyzer.py rapport.pdf --output analyse.txt
```

## ⚙️ Configuration (optionnel)

Créez un fichier `config.json` pour définir votre modèle par défaut :

```bash
cp config.example.json config.json
```

Éditez `config.json` :
```json
{
  "default_model": "llama3.1:8b"
}
```

## 📊 Quel modèle choisir ?

### Pour l'analyse générale en français
✅ **mistral:7b-instruct** - Excellent avec le français
```bash
python financial_analyzer.py rapport.pdf --model mistral:7b-instruct
```

### Pour la performance maximale
✅ **llama3.1:8b** - Très intelligent, bon raisonnement
```bash
python financial_analyzer.py rapport.pdf --model llama3.1:8b
```

### Pour les calculs complexes
✅ **qwen2.5-coder:7b** - Spécialisé en code et calculs
```bash
python financial_analyzer.py rapport.pdf --model qwen2.5-coder:7b
```

### Pour le raisonnement approfondi
✅ **deepseek-r1:8b** - Excellent pour analyser en profondeur
```bash
python financial_analyzer.py rapport.pdf --model deepseek-r1:8b
```

### Pour générer du code de calcul
✅ **codellama:7b** - Peut créer des scripts de calcul
```bash
python financial_analyzer.py rapport.pdf --model codellama:7b
```

### Pour l'équilibre vitesse/qualité
✅ **qwen2.5:7b** ou **qwen3:8b** - Bon compromis
```bash
python financial_analyzer.py rapport.pdf --model qwen2.5:7b
```

## 🔥 Exemples complets

### Analyser avec calculs de ratios uniquement

```bash
python financial_analyzer.py bilan.xlsx \
  --model llama3.1:8b \
  --calculations ratios \
  --output ratios_2024.txt
```

### Analyse multiple (tous vos rapports)

```bash
#!/bin/bash
for file in rapports/*.pdf; do
    echo "Analyse: $file"
    python financial_analyzer.py "$file" \
      --model mistral:7b-instruct \
      --output "analyses/$(basename "$file" .pdf).txt"
done
```

## 🐛 Dépannage rapide

### "Ollama n'est pas en cours d'exécution"
```bash
# Démarrez Ollama dans un autre terminal
ollama serve
```

### "Module ollama not found"
```bash
pip install ollama
```

### "Modèle non trouvé"
```bash
# Téléchargez le modèle
ollama pull mistral:7b-instruct
```

### Lister les modèles disponibles
```bash
python financial_analyzer.py --list-models
```

## 💡 Astuces

### 1. Vitesse vs Qualité

- **Rapide**: qwen2.5:7b, mistral:7b
- **Équilibré**: llama3.1:8b
- **Qualité max**: deepseek-r1:8b (plus lent)

### 2. Type d'analyse

- **Texte/Compréhension**: mistral, llama3.1
- **Calculs/Code**: qwen2.5-coder, codellama
- **Raisonnement**: deepseek-r1, llama3.1

### 3. Langue

- **Français**: mistral (excellent)
- **Multilingue**: llama3.1, qwen2.5

## 🚀 Mode Expert

### Combiner plusieurs analyses

```python
#!/usr/bin/env python3
from financial_analyzer import FinancialReportAnalyzer

# Analyser avec plusieurs modèles
models = ["mistral:7b-instruct", "llama3.1:8b", "qwen2.5-coder:7b"]

for model in models:
    print(f"\n=== Analyse avec {model} ===")
    analyzer = FinancialReportAnalyzer(backend="ollama", model=model)
    results = analyzer.process_report("rapport.pdf", calculations="all")
    print(results["analysis"])
```

### Utiliser en bibliothèque Python

```python
from financial_analyzer import FinancialReportAnalyzer

# Créer l'analyseur
analyzer = FinancialReportAnalyzer(
    backend="ollama",
    model="llama3.1:8b"
)

# Analyser un fichier
results = analyzer.process_report("rapport.pdf", calculations="ratios")

if results["success"]:
    print(results["analysis"])
else:
    print(f"Erreur: {results['error']}")
```

## 📚 Plus d'infos

- **Ollama**: https://ollama.ai
- **Modèles disponibles**: https://ollama.ai/library

## ✨ Vous êtes prêt !

Lancez votre première analyse :

```bash
python financial_analyzer.py --list-models
python financial_analyzer.py votre_fichier.pdf
```

Tout est local, gratuit, et privé ! 🎉
