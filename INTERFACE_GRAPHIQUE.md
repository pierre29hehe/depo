# 🖥️ Interface Graphique - Guide d'Utilisation

Interface graphique intuitive pour analyser vos rapports financiers en quelques clics !

## 🚀 Lancement Rapide

### Linux / macOS

```bash
# Méthode 1 : Script de lancement
./lancer_interface.sh

# Méthode 2 : Directement avec Python
python3 financial_analyzer_gui.py
```

### Windows

```bash
# Double-cliquez sur le fichier :
lancer_interface.bat

# Ou en ligne de commande :
python financial_analyzer_gui.py
```

## 📋 Guide d'Utilisation

### 1️⃣ Sélectionner un Fichier

Cliquez sur le bouton **"📁 Parcourir..."** pour ouvrir une fenêtre de navigation.

**Formats supportés :**
- 📄 PDF (`.pdf`)
- 📊 Excel (`.xlsx`, `.xls`)
- 📈 CSV (`.csv`)
- 📝 Texte (`.txt`)

Naviguez dans vos dossiers et sélectionnez votre rapport financier.

### 2️⃣ Choisir la Configuration

**Backend IA :**
- ☑️ **Ollama (Local - Gratuit)** - Recommandé
  - 100% gratuit
  - Vos données restent privées
  - Fonctionne hors ligne

- ☑️ **Open Interpreter (Local + Code)**
  - Peut exécuter du code pour calculs complexes
  - Analyse plus approfondie

- ☑️ **Claude AI (Cloud)**
  - Nécessite une clé API
  - Très performant

**Modèle :**
- Sélectionnez le modèle IA dans la liste déroulante
- Modèles recommandés :
  - `mistral:7b-instruct` - Excellent en français
  - `llama3.1:8b` - Très performant
  - `qwen2.5-coder:7b` - Spécialisé calculs

**Type de Calculs :**
- **all - Analyse complète** ✅ (Recommandé)
- **ratios - Ratios financiers** (Liquidité, solvabilité, etc.)
- **margins - Marges** (Brute, nette, EBITDA, etc.)
- **growth - Croissance** (Évolution CA, bénéfices)

### 3️⃣ Lancer l'Analyse

Cliquez sur le bouton **"🚀 Analyser le Rapport"**

L'analyse démarre et s'affiche en temps réel dans la zone de résultats.

⏱️ **Temps d'analyse :** 10 secondes à 2 minutes selon :
- Taille du fichier
- Modèle IA choisi
- Complexité du rapport

### 4️⃣ Sauvegarder les Résultats

Une fois l'analyse terminée :

1. Cliquez sur **"💾 Sauvegarder"**
2. Choisissez l'emplacement et le nom du fichier
3. Cliquez sur "Enregistrer"

✅ Le résultat est sauvegardé en format texte (`.txt`)

### 5️⃣ Analyser un Autre Fichier

- Cliquez sur **"🗑️ Effacer"** pour nettoyer les résultats
- Recommencez à l'étape 1

## 🎨 Captures d'Écran de l'Interface

```
┌─────────────────────────────────────────────────────────┐
│  📊 Analyseur de Rapports Financiers                   │
│  Analyse intelligente avec IA locale ou cloud           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  📄 Fichier à analyser                                  │
│  ┌────────────────────────────────────┐ ┌────────────┐ │
│  │ /chemin/vers/rapport.pdf           │ │📁 Parcourir│ │
│  └────────────────────────────────────┘ └────────────┘ │
│                                                          │
│  ⚙️ Configuration                                       │
│  Backend IA:                                            │
│  ○ Ollama  ○ Open Interpreter  ○ Claude AI             │
│                                                          │
│  Modèle: [mistral:7b-instruct      ▼]                  │
│  Calculs: [all - Analyse complète   ▼]                 │
│                                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                │
│  │🚀 Analyser│ │💾 Sauver │ │🗑️ Effacer│                │
│  └──────────┘ └──────────┘ └──────────┘                │
│                                                          │
│  📊 Résultats de l'analyse                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │ ════════════════════════════════════════════        │ │
│  │ 📊 ANALYSE DE RAPPORT FINANCIER                     │ │
│  │ ════════════════════════════════════════════        │ │
│  │                                                      │ │
│  │ 📄 Fichier: rapport.pdf                             │ │
│  │ 🤖 Backend: ollama                                  │ │
│  │ 🎯 Modèle: mistral:7b-instruct                      │ │
│  │                                                      │ │
│  │ ──────────────────────────────────────────          │ │
│  │ ANALYSE                                              │ │
│  │ ──────────────────────────────────────────          │ │
│  │                                                      │ │
│  │ **Résumé**                                          │ │
│  │ Rapport financier annuel 2024...                    │ │
│  │                                                      │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  Statut: ✅ Analyse terminée avec succès                │
└─────────────────────────────────────────────────────────┘
```

## ⚙️ Fonctionnalités de l'Interface

### ✅ Avantages

- 🖱️ **Facile à utiliser** - Navigation intuitive
- 📁 **Sélection visuelle** - Parcourir vos dossiers facilement
- ⚡ **Analyse en temps réel** - Voir les résultats immédiatement
- 💾 **Sauvegarde rapide** - Un clic pour sauvegarder
- 🎨 **Interface claire** - Design moderne et lisible
- 🔄 **Multi-analyses** - Analysez plusieurs fichiers successivement

### 🎯 Cas d'Usage

**Pour les comptables :**
```
1. Sélectionnez le bilan annuel (PDF)
2. Choisissez "ratios - Ratios financiers"
3. Analysez en 1 clic
4. Sauvegardez le rapport pour votre client
```

**Pour les analystes financiers :**
```
1. Sélectionnez le rapport financier (Excel)
2. Choisissez "all - Analyse complète"
3. Utilisez qwen2.5-coder pour calculs précis
4. Exportez les résultats
```

**Pour les entrepreneurs :**
```
1. Sélectionnez votre compte de résultat (CSV)
2. Choisissez "growth - Croissance"
3. Analysez l'évolution de votre entreprise
4. Partagez avec votre expert-comptable
```

## 🔧 Configuration Avancée

### Changer le Modèle par Défaut

Éditez `config.json` :
```json
{
  "default_model": "llama3.1:8b"
}
```

### Ajouter de Nouveaux Modèles

```bash
# Télécharger un nouveau modèle
ollama pull mistral:7b-instruct

# Le modèle apparaîtra automatiquement dans l'interface
```

## 🐛 Dépannage

### L'interface ne se lance pas

```bash
# Vérifier que tkinter est installé
python3 -c "import tkinter"

# Si erreur, installer tkinter (Linux)
sudo apt-get install python3-tk
```

### "Module financial_analyzer not found"

```bash
# Assurez-vous d'être dans le bon dossier
cd /home/user/depo
python3 financial_analyzer_gui.py
```

### Aucun modèle disponible

```bash
# Vérifier qu'Ollama tourne
ollama list

# Si erreur, lancer Ollama
ollama serve
```

### L'analyse ne démarre pas

1. Vérifiez qu'un fichier est bien sélectionné
2. Vérifiez qu'Ollama est lancé : `ollama serve`
3. Vérifiez le modèle sélectionné existe : `ollama list`

## 💡 Astuces

### 1. Glisser-Déposer (À venir)
Prochaine version permettra de glisser-déposer les fichiers !

### 2. Analyses Multiples
Gardez l'interface ouverte pour analyser plusieurs fichiers rapidement.

### 3. Comparer les Modèles
Analysez le même fichier avec différents modèles pour comparer les résultats !

### 4. Export Automatique
Sauvegardez toujours vos analyses pour garder un historique.

## 📚 Ressources

- **Guide complet** : [INSTALLATION_RAPIDE.md](INSTALLATION_RAPIDE.md)
- **Documentation** : [README.md](README.md)
- **Guide CLI** : [GUIDE_USAGE.md](GUIDE_USAGE.md)

## 🎓 Tutoriel Vidéo (À venir)

Un tutoriel vidéo sera bientôt disponible pour vous guider pas à pas !

## 🤝 Support

Besoin d'aide ?
1. Consultez ce guide
2. Vérifiez que Ollama est lancé
3. Testez avec le fichier `rapport_test.txt`

---

**Interface développée pour une utilisation simple et intuitive** ✨
