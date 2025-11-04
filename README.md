# Analyseur de Rapports Financiers avec IA

Programme Python qui utilise l'intelligence artificielle pour lire et analyser des rapports financiers automatiquement.

## Fonctionnalités

- 📄 **Lecture multi-format** : Support des fichiers PDF, Excel (XLSX/XLS), et CSV
- 🤖 **Analyse IA** : Utilise Claude AI pour extraire et analyser les données financières
- 🧮 **Calculs automatiques** : Ratios financiers, marges, croissance, etc.
- 📊 **Rapport détaillé** : Génération d'un rapport d'analyse complet

## Installation

### 1. Installer Python 3.8+

Assurez-vous d'avoir Python 3.8 ou plus récent installé.

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configuration

Créez un fichier `config.json` à partir de l'exemple :

```bash
cp config.example.json config.json
```

Éditez `config.json` et ajoutez votre clé API Anthropic :

```json
{
  "anthropic_api_key": "votre-clé-api-ici"
}
```

Pour obtenir une clé API gratuite : https://console.anthropic.com/

## Utilisation

### Analyse simple

```bash
python financial_analyzer.py rapport.pdf
```

### Avec options

```bash
python financial_analyzer.py rapport.xlsx --output analyse.txt --format json
```

### Options disponibles

- `--output` : Fichier de sortie pour le rapport (défaut: console)
- `--format` : Format de sortie (text/json, défaut: text)
- `--calculations` : Types de calculs à effectuer (ratios/margins/growth/all)

## Exemples de calculs

Le programme peut calculer automatiquement :

- **Ratios de liquidité** : Ratio courant, ratio rapide
- **Ratios de rentabilité** : Marge brute, marge nette, ROE, ROA
- **Ratios d'endettement** : Ratio dette/actifs, ratio de couverture
- **Analyse de croissance** : Évolution du CA, des bénéfices
- **Analyse des flux de trésorerie**

## Formats de rapports supportés

- **PDF** : Rapports financiers, états financiers
- **Excel** : Feuilles de calcul, bilans, compte de résultat
- **CSV** : Données tabulaires, exports comptables

## Dépannage

### Erreur "API key not found"
Vérifiez que le fichier `config.json` existe et contient votre clé API.

### Erreur lors de la lecture PDF
Installez poppler-utils : `sudo apt-get install poppler-utils` (Linux)

## Licence

MIT
