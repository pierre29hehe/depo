#!/bin/bash
# Script de lancement de l'extracteur de tableaux PDF

echo "🚀 Lancement de l'extracteur de tableaux PDF..."
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

# Vérifier les dépendances
echo "📦 Vérification des dépendances..."
python3 -c "import pdfplumber, pandas, tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installation des dépendances manquantes..."
    pip install pdfplumber pandas openpyxl
fi

# Lancer le programme
echo "✅ Lancement de l'interface..."
python3 pdf_table_extractor.py
