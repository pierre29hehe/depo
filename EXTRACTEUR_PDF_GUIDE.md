# 📊 Extracteur de Tableaux PDF - Guide d'utilisation

## 🎯 Description

Programme simple et direct pour extraire les tableaux de documents financiers PDF **sans utiliser l'IA**.

### ✅ Avantages
- ✨ **Aucune perte de données** - Extraction directe des tableaux
- 🚀 **Rapide** - Pas d'appel à des modèles IA
- 🔍 **Détection automatique** - Identifie le type de données (bilan, compte de résultat, etc.)
- 💾 **Export multiple** - Texte et Excel
- 🖥️ **Interface simple** - Facile à utiliser

---

## 🚀 Démarrage rapide

### Windows
Double-cliquez sur : `lancer_extracteur.bat`

### Linux / Mac
```bash
./lancer_extracteur.sh
```

### Manuel
```bash
python3 pdf_table_extractor.py
```

---

## 📖 Utilisation

### 1. Lancer le programme
- Double-cliquez sur le script de lancement
- Ou lancez depuis le terminal

### 2. Sélectionner un fichier PDF
- Cliquez sur **"📁 Sélectionner PDF..."**
- Choisissez votre document financier (bilan, compte de résultat, etc.)

### 3. Extraire les tableaux
- Cliquez sur **"🚀 Extraire les Tableaux"**
- Les tableaux sont extraits et affichés immédiatement

### 4. Consulter les résultats
Chaque tableau affiche :
- 📍 **Position** : Page et numéro du tableau
- 📊 **Type détecté** : Compte de résultat, Bilan, Flux de trésorerie, etc.
- 📏 **Dimensions** : Nombre de lignes et colonnes
- 📋 **Données** : Contenu complet du tableau

### 5. Sauvegarder
- **💾 Sauvegarder** : Export en fichier texte (.txt)
- **📊 Exporter Excel** : Export en fichier Excel (.xlsx) avec un onglet par tableau

---

## 🔍 Types de tableaux détectés

Le programme identifie automatiquement :

| Icône | Type | Mots-clés détectés |
|-------|------|-------------------|
| 📊 | **Compte de Résultat** | Chiffre d'affaires, revenus, bénéfice, EBITDA, charges |
| 💰 | **Bilan** | Actif, passif, capitaux propres, immobilisations, trésorerie |
| 💸 | **Flux de Trésorerie** | Cash flow, variation de trésorerie, activités opérationnelles |
| 📈 | **Ratios Financiers** | Ratio, marge, rentabilité, liquidité, % |
| 📅 | **Données Temporelles** | Années, trimestres, périodes |
| 📋 | **Tableau Général** | Autres tableaux |

---

## 💡 Exemples d'utilisation

### Analyser un bilan comptable
1. Ouvrez le PDF du bilan
2. Extrayez les tableaux
3. Le programme détecte automatiquement :
   - Le bilan actif/passif (💰)
   - Le compte de résultat (📊)
   - Les annexes (📋)

### Extraire des rapports financiers
1. Chargez le rapport annuel PDF
2. Tous les tableaux sont extraits page par page
3. Exportez en Excel pour analyse dans un tableur

### Comparer plusieurs périodes
1. Extrayez les tableaux de plusieurs rapports
2. Sauvegardez chaque résultat
3. Comparez les données dans Excel

---

## 🛠️ Installation manuelle des dépendances

Si le script automatique ne fonctionne pas :

```bash
pip install pdfplumber pandas openpyxl
```

### Dépendances requises
- `pdfplumber` - Extraction de tableaux PDF
- `pandas` - Manipulation de données
- `openpyxl` - Export Excel
- `tkinter` - Interface graphique (généralement inclus avec Python)

---

## ❓ Dépannage

### Le programme ne se lance pas
- Vérifiez que Python 3 est installé : `python3 --version`
- Installez les dépendances : `pip install pdfplumber pandas openpyxl`

### Aucun tableau n'est détecté
- Vérifiez que le PDF contient des tableaux structurés
- Certains PDF scannés (images) ne sont pas supportés
- Essayez d'ouvrir le PDF avec un lecteur PDF pour vérifier

### Erreur d'encodage
- Le programme utilise UTF-8 par défaut
- Pour les caractères spéciaux, vérifiez que votre PDF est encodé correctement

### Export Excel échoue
- Vérifiez que `openpyxl` est installé : `pip install openpyxl`
- Vérifiez que vous avez les droits d'écriture dans le dossier

---

## 🆚 Différence avec l'ancien programme

| Caractéristique | Ancien (avec IA) | Nouveau (sans IA) |
|-----------------|------------------|-------------------|
| **Extraction** | Via modèle IA | Directe |
| **Perte de données** | Possible | ❌ Aucune |
| **Vitesse** | Lente (dépend du modèle) | ⚡ Rapide |
| **Précision** | Dépend du modèle | ✅ 100% des tableaux |
| **Analyse** | Oui | Non (données brutes) |
| **Dépendances** | Ollama / Anthropic | Seulement pdfplumber |

---

## 📝 Notes

- Les tableaux sont extraits **exactement comme ils apparaissent** dans le PDF
- Aucune interprétation ou analyse n'est faite par l'IA
- Les données brutes sont conservées intégralement
- Pour une analyse, vous pouvez ensuite utiliser Excel ou un autre outil

---

## 📧 Support

En cas de problème :
1. Vérifiez que toutes les dépendances sont installées
2. Testez avec un PDF simple contenant des tableaux
3. Vérifiez les messages d'erreur dans la console

---

**Version** : 1.0
**Date** : 2025-11-05
**Auteur** : Extracteur PDF Direct
