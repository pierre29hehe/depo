#!/usr/bin/env python3
"""
Analyseur de Rapports Financiers avec IA
Utilise Claude AI pour analyser des rapports financiers et effectuer des calculs
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Imports pour la lecture de fichiers
try:
    import PyPDF2
    import pdfplumber
    import pandas as pd
    from anthropic import Anthropic
except ImportError as e:
    print(f"❌ Erreur: Dépendance manquante. Exécutez: pip install -r requirements.txt")
    print(f"   Détail: {e}")
    sys.exit(1)


class FinancialReportAnalyzer:
    """Analyseur de rapports financiers utilisant l'IA"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialise l'analyseur avec une clé API Anthropic

        Args:
            api_key: Clé API Anthropic (ou None pour charger depuis config.json)
        """
        if api_key is None:
            api_key = self._load_api_key()

        if not api_key:
            raise ValueError(
                "Clé API Anthropic non trouvée. "
                "Créez un fichier config.json avec votre clé API."
            )

        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def _load_api_key(self) -> Optional[str]:
        """Charge la clé API depuis config.json ou variables d'environnement"""
        # Essayer config.json
        config_path = Path("config.json")
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = json.load(f)
                    return config.get("anthropic_api_key")
            except Exception as e:
                print(f"⚠️  Avertissement: Erreur lecture config.json: {e}")

        # Essayer variable d'environnement
        return os.environ.get("ANTHROPIC_API_KEY")

    def read_file(self, file_path: str) -> str:
        """
        Lit un fichier financier et extrait le texte

        Args:
            file_path: Chemin vers le fichier

        Returns:
            Texte extrait du fichier
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Fichier non trouvé: {file_path}")

        extension = path.suffix.lower()

        print(f"📄 Lecture du fichier: {path.name}")

        if extension == '.pdf':
            return self._read_pdf(path)
        elif extension in ['.xlsx', '.xls']:
            return self._read_excel(path)
        elif extension == '.csv':
            return self._read_csv(path)
        else:
            # Essayer de lire comme texte brut
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                raise ValueError(f"Format de fichier non supporté: {extension}")

    def _read_pdf(self, path: Path) -> str:
        """Extrait le texte d'un PDF"""
        text_parts = []

        try:
            # Essayer avec pdfplumber (meilleur pour les tableaux)
            with pdfplumber.open(path) as pdf:
                for i, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(f"--- Page {i} ---\n{page_text}")

                    # Extraire les tableaux
                    tables = page.extract_tables()
                    for j, table in enumerate(tables, 1):
                        if table:
                            text_parts.append(f"\n[Tableau {j}]")
                            for row in table:
                                text_parts.append(" | ".join(str(cell or "") for cell in row))
        except Exception as e:
            print(f"⚠️  pdfplumber a échoué, essai avec PyPDF2...")
            # Fallback sur PyPDF2
            with open(path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for i, page in enumerate(pdf_reader.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(f"--- Page {i} ---\n{page_text}")

        return "\n\n".join(text_parts)

    def _read_excel(self, path: Path) -> str:
        """Extrait le texte d'un fichier Excel"""
        text_parts = []

        # Lire toutes les feuilles
        excel_file = pd.ExcelFile(path)

        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(path, sheet_name=sheet_name)
            text_parts.append(f"=== Feuille: {sheet_name} ===")
            text_parts.append(df.to_string())
            text_parts.append("")

        return "\n".join(text_parts)

    def _read_csv(self, path: Path) -> str:
        """Extrait le texte d'un fichier CSV"""
        df = pd.read_csv(path)
        return df.to_string()

    def analyze_financial_report(
        self,
        text: str,
        calculations: str = "all"
    ) -> Dict:
        """
        Analyse un rapport financier avec l'IA

        Args:
            text: Texte du rapport financier
            calculations: Types de calculs ('ratios', 'margins', 'growth', 'all')

        Returns:
            Dictionnaire contenant l'analyse
        """
        print(f"🤖 Analyse du rapport avec Claude AI...")

        # Définir le prompt selon les calculs demandés
        calculation_prompts = {
            "ratios": "calcule tous les ratios financiers pertinents (liquidité, solvabilité, etc.)",
            "margins": "calcule les marges (brute, nette, opérationnelle, EBITDA)",
            "growth": "analyse la croissance (revenus, bénéfices, évolution annuelle)",
            "all": "effectue une analyse complète avec tous les calculs et ratios financiers"
        }

        calc_instruction = calculation_prompts.get(calculations, calculation_prompts["all"])

        prompt = f"""Analyse ce rapport financier en français et {calc_instruction}.

Rapport financier:
{text[:15000]}  # Limiter à 15000 caractères pour l'API

Pour ton analyse:
1. **Résumé**: Identifie le type de document et la période couverte
2. **Données clés**: Extrait les principaux chiffres (revenus, bénéfices, actifs, passifs, etc.)
3. **Calculs**: Effectue les calculs demandés avec les formules utilisées
4. **Analyse**: Interprète les résultats et identifie les points importants
5. **Recommandations**: Suggère des points d'attention ou d'amélioration

Présente les résultats de manière structurée et claire."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            analysis_text = response.content[0].text

            return {
                "success": True,
                "analysis": analysis_text,
                "model": self.model,
                "tokens_used": response.usage.input_tokens + response.usage.output_tokens
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def process_report(
        self,
        file_path: str,
        calculations: str = "all"
    ) -> Dict:
        """
        Traite un rapport financier complet

        Args:
            file_path: Chemin vers le fichier
            calculations: Types de calculs à effectuer

        Returns:
            Résultats de l'analyse
        """
        try:
            # Lire le fichier
            text = self.read_file(file_path)

            if not text.strip():
                return {
                    "success": False,
                    "error": "Le fichier est vide ou n'a pas pu être lu"
                }

            print(f"✅ {len(text)} caractères extraits")

            # Analyser avec l'IA
            results = self.analyze_financial_report(text, calculations)

            # Ajouter les métadonnées
            results["file"] = file_path
            results["file_size"] = os.path.getsize(file_path)
            results["text_length"] = len(text)

            return results

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "file": file_path
            }


def format_output(results: Dict, format_type: str = "text") -> str:
    """
    Formate les résultats pour l'affichage

    Args:
        results: Résultats de l'analyse
        format_type: Format de sortie ('text' ou 'json')

    Returns:
        Résultats formatés
    """
    if format_type == "json":
        return json.dumps(results, indent=2, ensure_ascii=False)

    # Format texte
    output = []
    output.append("=" * 80)
    output.append("📊 ANALYSE DE RAPPORT FINANCIER")
    output.append("=" * 80)
    output.append("")

    if not results.get("success"):
        output.append(f"❌ ERREUR: {results.get('error', 'Erreur inconnue')}")
        return "\n".join(output)

    output.append(f"📄 Fichier: {results.get('file', 'N/A')}")
    output.append(f"📏 Taille: {results.get('file_size', 0):,} octets")
    output.append(f"📝 Texte extrait: {results.get('text_length', 0):,} caractères")
    output.append(f"🤖 Modèle: {results.get('model', 'N/A')}")
    output.append(f"🎯 Tokens utilisés: {results.get('tokens_used', 'N/A'):,}")
    output.append("")
    output.append("-" * 80)
    output.append("ANALYSE")
    output.append("-" * 80)
    output.append("")
    output.append(results.get('analysis', 'Aucune analyse disponible'))
    output.append("")
    output.append("=" * 80)

    return "\n".join(output)


def main():
    """Point d'entrée principal du programme"""
    parser = argparse.ArgumentParser(
        description="Analyseur de rapports financiers avec IA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python financial_analyzer.py rapport.pdf
  python financial_analyzer.py bilan.xlsx --calculations ratios
  python financial_analyzer.py data.csv --output analyse.txt --format json
        """
    )

    parser.add_argument(
        "file",
        help="Chemin vers le rapport financier (PDF, Excel, CSV)"
    )

    parser.add_argument(
        "--output", "-o",
        help="Fichier de sortie (défaut: affichage console)",
        default=None
    )

    parser.add_argument(
        "--format", "-f",
        choices=["text", "json"],
        default="text",
        help="Format de sortie (défaut: text)"
    )

    parser.add_argument(
        "--calculations", "-c",
        choices=["ratios", "margins", "growth", "all"],
        default="all",
        help="Types de calculs à effectuer (défaut: all)"
    )

    args = parser.parse_args()

    # Créer l'analyseur
    try:
        analyzer = FinancialReportAnalyzer()
    except ValueError as e:
        print(f"❌ {e}")
        print("\n💡 Pour obtenir une clé API gratuite:")
        print("   1. Visitez: https://console.anthropic.com/")
        print("   2. Créez un compte et générez une clé API")
        print("   3. Créez un fichier config.json avec:")
        print('      {"anthropic_api_key": "votre-clé-ici"}')
        sys.exit(1)

    # Traiter le rapport
    print(f"\n🚀 Démarrage de l'analyse...")
    results = analyzer.process_report(args.file, args.calculations)

    # Formater les résultats
    output = format_output(results, args.format)

    # Afficher ou sauvegarder
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"\n✅ Analyse sauvegardée dans: {args.output}")
        except Exception as e:
            print(f"\n❌ Erreur lors de la sauvegarde: {e}")
            print("\n" + output)
    else:
        print("\n" + output)

    # Code de sortie
    sys.exit(0 if results.get("success") else 1)


if __name__ == "__main__":
    main()
