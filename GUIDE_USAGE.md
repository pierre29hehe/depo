# Guide d'Utilisation - Analyseur de Rapports Financiers

## Installation Rapide

### Étape 1: Installer les dépendances

```bash
pip install -r requirements.txt
```

### Étape 2: Configurer la clé API

1. Créez votre fichier de configuration:
```bash
cp config.example.json config.json
```

2. Obtenez une clé API Anthropic:
   - Visitez: https://console.anthropic.com/
   - Créez un compte (gratuit)
   - Générez une clé API

3. Éditez `config.json` et ajoutez votre clé:
```json
{
  "anthropic_api_key": "sk-ant-api03-votre-cle-ici"
}
```

## Exemples d'Utilisation

### 1. Analyse simple d'un PDF

```bash
python financial_analyzer.py rapport_annuel.pdf
```

**Sortie**: Affiche l'analyse complète dans la console

### 2. Analyser un fichier Excel avec sauvegarde

```bash
python financial_analyzer.py bilan_2024.xlsx --output resultat.txt
```

**Sortie**: Sauvegarde l'analyse dans `resultat.txt`

### 3. Calculer uniquement les ratios

```bash
python financial_analyzer.py rapport.pdf --calculations ratios
```

**Options de calculs**:
- `ratios` : Ratios de liquidité, solvabilité, etc.
- `margins` : Marges (brute, nette, opérationnelle)
- `growth` : Analyse de croissance
- `all` : Analyse complète (défaut)

### 4. Exporter en JSON

```bash
python financial_analyzer.py data.csv --format json --output analyse.json
```

**Sortie**: Fichier JSON structuré pour traitement automatique

### 5. Analyser plusieurs fichiers (script bash)

```bash
#!/bin/bash
for file in rapports/*.pdf; do
    echo "Analyse de $file..."
    python financial_analyzer.py "$file" --output "analyses/$(basename $file .pdf).txt"
done
```

## Types de Rapports Supportés

### Formats de fichiers
- ✅ **PDF** (.pdf) - Rapports annuels, états financiers
- ✅ **Excel** (.xlsx, .xls) - Bilans, comptes de résultat
- ✅ **CSV** (.csv) - Données tabulaires

### Types de documents
- Rapports annuels
- Bilans comptables
- Comptes de résultat
- Tableaux de flux de trésorerie
- États financiers consolidés
- Rapports trimestriels

## Ce que l'IA Peut Calculer

### Ratios de Liquidité
- Ratio de liquidité générale (Current Ratio)
- Ratio de liquidité réduite (Quick Ratio)
- Ratio de trésorerie immédiate

### Ratios de Rentabilité
- Marge brute
- Marge nette
- Marge opérationnelle
- Marge EBITDA
- ROE (Return on Equity)
- ROA (Return on Assets)
- ROI (Return on Investment)

### Ratios d'Endettement
- Ratio dette/capitaux propres
- Ratio dette/actifs
- Ratio de couverture des intérêts
- Ratio de couverture du service de la dette

### Ratios d'Activité
- Rotation des stocks
- Rotation des créances clients
- Rotation des actifs

### Analyse de Croissance
- Croissance du chiffre d'affaires
- Croissance des bénéfices
- Évolution des marges
- Taux de croissance annuel composé (CAGR)

## Exemples de Sorties

### Format Texte (défaut)

```
================================================================================
📊 ANALYSE DE RAPPORT FINANCIER
================================================================================

📄 Fichier: rapport_2024.pdf
📏 Taille: 245,632 octets
📝 Texte extrait: 15,234 caractères
🤖 Modèle: claude-3-5-sonnet-20241022
🎯 Tokens utilisés: 8,456

--------------------------------------------------------------------------------
ANALYSE
--------------------------------------------------------------------------------

**Résumé**
Rapport financier annuel pour l'exercice 2024...

**Données Clés**
- Chiffre d'affaires: 125.5M€ (+12% vs 2023)
- Résultat net: 18.2M€ (+8% vs 2023)
- Total actifs: 95.3M€
...
```

### Format JSON

```json
{
  "success": true,
  "file": "rapport_2024.pdf",
  "analysis": "...",
  "model": "claude-3-5-sonnet-20241022",
  "tokens_used": 8456
}
```

## Dépannage

### ❌ "Clé API non trouvée"

**Solution**: Vérifiez que `config.json` existe et contient votre clé API

```bash
cat config.json
# Devrait afficher: {"anthropic_api_key": "sk-ant-..."}
```

### ❌ "Module 'anthropic' not found"

**Solution**: Installez les dépendances

```bash
pip install -r requirements.txt
```

### ❌ "Fichier non trouvé"

**Solution**: Vérifiez le chemin du fichier

```bash
# Chemin relatif
python financial_analyzer.py ./rapports/fichier.pdf

# Chemin absolu
python financial_analyzer.py /home/user/Documents/fichier.pdf
```

### ❌ Erreur lors de la lecture PDF

**Solution (Linux)**: Installez poppler-utils

```bash
sudo apt-get install poppler-utils
```

**Solution (Windows)**: Téléchargez poppler depuis https://github.com/oschwartz10612/poppler-windows

### ⚠️ "Texte extrait est vide"

**Causes possibles**:
1. PDF scanné (image) sans OCR
2. PDF protégé par mot de passe
3. Fichier corrompu

**Solution**: Essayez de réexporter le PDF ou utilisez un outil OCR

## Conseils d'Utilisation

### Pour de meilleurs résultats:

1. **Qualité du fichier**: Utilisez des PDFs générés électroniquement plutôt que scannés
2. **Structure claire**: Les fichiers bien structurés donnent de meilleurs résultats
3. **Données complètes**: Incluez tous les tableaux et notes nécessaires
4. **Période claire**: Mentionnez la période couverte dans le document

### Limites:

- Fichiers très volumineux (>50 pages): L'analyse peut être partielle
- PDFs scannés: Nécessitent l'OCR préalable
- Formats propriétaires: Convertir en PDF/Excel/CSV d'abord

## Automatisation

### Script pour analyse en masse

```python
#!/usr/bin/env python3
import os
import glob
from financial_analyzer import FinancialReportAnalyzer

analyzer = FinancialReportAnalyzer()

for file in glob.glob("rapports/*.pdf"):
    print(f"Traitement: {file}")
    results = analyzer.process_report(file, calculations="all")

    if results["success"]:
        output_file = f"analyses/{os.path.basename(file)}.txt"
        with open(output_file, 'w') as f:
            f.write(results["analysis"])
        print(f"✅ Sauvegardé: {output_file}")
    else:
        print(f"❌ Erreur: {results['error']}")
```

## Support

Pour toute question ou problème:
1. Consultez ce guide
2. Vérifiez les messages d'erreur
3. Assurez-vous que toutes les dépendances sont installées

## Ressources

- Documentation Anthropic: https://docs.anthropic.com/
- API Claude: https://console.anthropic.com/
- GitHub Issues: (Ajoutez votre lien ici)
