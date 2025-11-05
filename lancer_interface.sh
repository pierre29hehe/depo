#!/bin/bash
# Script de lancement de l'interface graphique

echo "🚀 Lancement de l'interface graphique..."
echo ""

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

# Lancer l'interface
python3 financial_analyzer_gui.py
