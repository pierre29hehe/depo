#!/usr/bin/env python3
"""
Analyseur de Rapports Financiers avec IA
Supporte les modèles locaux (Ollama) et cloud (Anthropic)
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import subprocess

# Imports pour la lecture de fichiers
try:
    import PyPDF2
    import pdfplumber
    import pandas as pd
except ImportError as e:
    print(f"❌ Erreur: Dépendance manquante. Exécutez: pip install -r requirements.txt")
    print(f"   Détail: {e}")
    sys.exit(1)


class AIBackend:
    """Classe de base pour les backends d'IA"""

    def __init__(self, model_name: str):
        self.model_name = model_name

    def analyze(self, prompt: str) -> Dict:
        raise NotImplementedError


class OllamaBackend(AIBackend):
    """Backend pour Ollama (modèles locaux)"""

    def __init__(self, model_name: str = "mistral:7b-instruct"):
        super().__init__(model_name)
        try:
            import ollama
            self.client = ollama
            self.available = True
        except ImportError:
            self.available = False
            print("⚠️  Module ollama non installé. Utilisez: pip install ollama")

    def check_ollama_running(self) -> bool:
        """Vérifie si Ollama est en cours d'exécution"""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False

    def list_models(self) -> List[str]:
        """Liste les modèles disponibles dans Ollama"""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                models = [line.split()[0] for line in lines if line.strip()]
                return models
            return []
        except Exception as e:
            print(f"⚠️  Erreur lors de la liste des modèles: {e}")
            return []

    def analyze(self, prompt: str) -> Dict:
        """Analyse avec Ollama"""
        if not self.available:
            return {
                "success": False,
                "error": "Module ollama non disponible"
            }

        if not self.check_ollama_running():
            return {
                "success": False,
                "error": "Ollama n'est pas en cours d'exécution. Lancez: ollama serve"
            }

        try:
            print(f"🤖 Analyse avec {self.model_name} (Ollama local)...")

            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )

            return {
                "success": True,
                "analysis": response['message']['content'],
                "model": self.model_name,
                "backend": "ollama"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur Ollama: {str(e)}"
            }


class OpenInterpreterBackend(AIBackend):
    """Backend pour Open Interpreter"""

    def __init__(self, model_name: str = "ollama/mistral:7b-instruct"):
        super().__init__(model_name)
        try:
            import interpreter
            self.interpreter = interpreter
            self.interpreter.llm.model = model_name
            self.interpreter.auto_run = True
            self.interpreter.offline = True  # Mode local
            self.available = True
        except ImportError:
            self.available = False
            print("⚠️  Module interpreter non installé. Utilisez: pip install open-interpreter")

    def analyze(self, prompt: str) -> Dict:
        """Analyse avec Open Interpreter"""
        if not self.available:
            return {
                "success": False,
                "error": "Module open-interpreter non disponible"
            }

        try:
            print(f"🤖 Analyse avec Open Interpreter ({self.model_name})...")

            # Open Interpreter peut exécuter du code pour faire les calculs
            enhanced_prompt = f"""
{prompt}

Si nécessaire, écris et exécute du code Python pour effectuer les calculs financiers.
Utilise pandas, numpy pour les calculs complexes.
"""

            messages = self.interpreter.chat(enhanced_prompt, display=False, stream=False)

            # Extraire le texte de la réponse
            analysis_text = ""
            for msg in messages:
                if msg.get("type") == "message" and msg.get("role") == "assistant":
                    analysis_text += msg.get("content", "")

            return {
                "success": True,
                "analysis": analysis_text,
                "model": self.model_name,
                "backend": "open-interpreter"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur Open Interpreter: {str(e)}"
            }


class AnthropicBackend(AIBackend):
    """Backend pour Anthropic Claude (cloud)"""

    def __init__(self, api_key: str, model_name: str = "claude-3-5-sonnet-20241022"):
        super().__init__(model_name)
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)
            self.available = True
        except ImportError:
            self.available = False
            print("⚠️  Module anthropic non installé. Utilisez: pip install anthropic")

    def analyze(self, prompt: str) -> Dict:
        """Analyse avec Claude"""
        if not self.available:
            return {
                "success": False,
                "error": "Module anthropic non disponible"
            }

        try:
            print(f"🤖 Analyse avec Claude AI ({self.model_name})...")

            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return {
                "success": True,
                "analysis": response.content[0].text,
                "model": self.model_name,
                "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
                "backend": "anthropic"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur Anthropic: {str(e)}"
            }


class FinancialReportAnalyzer:
    """Analyseur de rapports financiers utilisant l'IA"""

    def __init__(
        self,
        backend: str = "ollama",
        model: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialise l'analyseur

        Args:
            backend: 'ollama', 'open-interpreter', ou 'anthropic'
            model: Nom du modèle à utiliser
            api_key: Clé API (pour Anthropic)
        """
        self.backend_type = backend

        # Charger la configuration
        config = self._load_config()

        # Initialiser le backend approprié
        if backend == "ollama":
            model = model or config.get("default_model", "mistral:7b-instruct")
            self.backend = OllamaBackend(model)
        elif backend == "open-interpreter":
            model = model or f"ollama/{config.get('default_model', 'mistral:7b-instruct')}"
            self.backend = OpenInterpreterBackend(model)
        elif backend == "anthropic":
            api_key = api_key or config.get("anthropic_api_key") or os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("Clé API Anthropic requise pour ce backend")
            model = model or config.get("anthropic_model", "claude-3-5-sonnet-20241022")
            self.backend = AnthropicBackend(api_key, model)
        else:
            raise ValueError(f"Backend non supporté: {backend}")

    def _load_config(self) -> Dict:
        """Charge la configuration depuis config.json"""
        config_path = Path("config.json")
        if config_path.exists():
            try:
                with open(config_path) as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Erreur lecture config.json: {e}")
        return {}

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
        # Définir le prompt selon les calculs demandés
        calculation_prompts = {
            "ratios": "calcule tous les ratios financiers pertinents (liquidité, solvabilité, etc.)",
            "margins": "calcule les marges (brute, nette, opérationnelle, EBITDA)",
            "growth": "analyse la croissance (revenus, bénéfices, évolution annuelle)",
            "all": "effectue une analyse complète avec tous les calculs et ratios financiers"
        }

        calc_instruction = calculation_prompts.get(calculations, calculation_prompts["all"])

        # Limiter la taille du texte selon le backend
        max_chars = 50000 if self.backend_type == "ollama" else 15000
        truncated_text = text[:max_chars]

        prompt = f"""Analyse ce rapport financier en français et {calc_instruction}.

Rapport financier:
{truncated_text}

Pour ton analyse:
1. **Résumé**: Identifie le type de document et la période couverte
2. **Données clés**: Extrait les principaux chiffres (revenus, bénéfices, actifs, passifs, etc.)
3. **Calculs**: Effectue les calculs demandés avec les formules utilisées
4. **Analyse**: Interprète les résultats et identifie les points importants
5. **Recommandations**: Suggère des points d'attention ou d'amélioration

Présente les résultats de manière structurée et claire en français."""

        return self.backend.analyze(prompt)

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
    output.append(f"🤖 Backend: {results.get('backend', 'N/A')}")
    output.append(f"🎯 Modèle: {results.get('model', 'N/A')}")

    if 'tokens_used' in results:
        output.append(f"💰 Tokens utilisés: {results.get('tokens_used', 'N/A'):,}")

    output.append("")
    output.append("-" * 80)
    output.append("ANALYSE")
    output.append("-" * 80)
    output.append("")
    output.append(results.get('analysis', 'Aucune analyse disponible'))
    output.append("")
    output.append("=" * 80)

    return "\n".join(output)


def list_ollama_models():
    """Liste les modèles Ollama disponibles"""
    backend = OllamaBackend()
    models = backend.list_models()

    if models:
        print("\n📋 Modèles Ollama disponibles:")
        for model in models:
            print(f"   - {model}")
    else:
        print("\n❌ Aucun modèle Ollama trouvé ou Ollama non installé")
        print("   Installez Ollama: https://ollama.ai")
        print("   Puis téléchargez un modèle: ollama pull mistral:7b-instruct")


def main():
    """Point d'entrée principal du programme"""
    parser = argparse.ArgumentParser(
        description="Analyseur de rapports financiers avec IA (local ou cloud)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  # Avec Ollama (local - par défaut)
  python financial_analyzer.py rapport.pdf
  python financial_analyzer.py rapport.pdf --model llama3.1:8b

  # Avec Open Interpreter
  python financial_analyzer.py rapport.pdf --backend open-interpreter

  # Avec Claude (cloud)
  python financial_analyzer.py rapport.pdf --backend anthropic

  # Lister les modèles Ollama disponibles
  python financial_analyzer.py --list-models

  # Avec options
  python financial_analyzer.py bilan.xlsx --calculations ratios --output resultat.txt
        """
    )

    parser.add_argument(
        "file",
        nargs="?",
        help="Chemin vers le rapport financier (PDF, Excel, CSV)"
    )

    parser.add_argument(
        "--backend", "-b",
        choices=["ollama", "open-interpreter", "anthropic"],
        default="ollama",
        help="Backend IA à utiliser (défaut: ollama)"
    )

    parser.add_argument(
        "--model", "-m",
        help="Modèle spécifique à utiliser"
    )

    parser.add_argument(
        "--list-models",
        action="store_true",
        help="Afficher les modèles Ollama disponibles"
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

    # Si --list-models, afficher et quitter
    if args.list_models:
        list_ollama_models()
        sys.exit(0)

    # Vérifier qu'un fichier est fourni
    if not args.file:
        parser.print_help()
        print("\n❌ Erreur: Vous devez fournir un fichier à analyser")
        sys.exit(1)

    # Créer l'analyseur
    try:
        analyzer = FinancialReportAnalyzer(
            backend=args.backend,
            model=args.model
        )
    except ValueError as e:
        print(f"❌ {e}")
        if args.backend == "anthropic":
            print("\n💡 Pour utiliser Anthropic Claude:")
            print("   1. Visitez: https://console.anthropic.com/")
            print("   2. Créez un fichier config.json avec:")
            print('      {"anthropic_api_key": "votre-clé-ici"}')
        elif args.backend == "ollama":
            print("\n💡 Pour utiliser Ollama:")
            print("   1. Installez Ollama: https://ollama.ai")
            print("   2. Lancez: ollama serve")
            print("   3. Téléchargez un modèle: ollama pull mistral:7b-instruct")
            print("\n   Modèles recommandés:")
            print("   - mistral:7b-instruct (général)")
            print("   - llama3.1:8b (performant)")
            print("   - qwen2.5-coder:7b (calculs)")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        sys.exit(1)

    # Traiter le rapport
    print(f"\n🚀 Démarrage de l'analyse avec {args.backend}...")
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
