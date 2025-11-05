#!/usr/bin/env python3
"""
Extracteur simple de tableaux PDF - Sans IA
Extrait les tableaux et identifie automatiquement les types de données
"""

import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
import PyPDF2
import re
from pathlib import Path
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class PDFTableExtractor:
    """Extracteur de tableaux PDF simple et direct"""

    def __init__(self):
        self.tables_data = []
        self.file_path = None

    def extract_tables(self, pdf_path):
        """Extrait le texte et détecte les tableaux d'un PDF"""
        self.file_path = pdf_path
        self.tables_data = []

        print(f"📄 Ouverture du PDF: {Path(pdf_path).name}")

        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)

            for page_num in range(total_pages):
                print(f"   Page {page_num + 1}/{total_pages}...")

                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()

                if page_text:
                    # Détecter les tableaux basés sur la structure du texte
                    detected_tables = self._detect_tables_in_text(page_text)

                    for table_num, table_data in enumerate(detected_tables, 1):
                        # Identifier le type de tableau
                        table_type = self._identify_table_type_simple(table_data)

                        # Stocker les données
                        self.tables_data.append({
                            'page': page_num + 1,
                            'table_num': table_num,
                            'type': table_type,
                            'content': table_data,
                            'raw_text': page_text
                        })

        # Si aucun tableau détecté, créer une entrée pour chaque page
        if not self.tables_data:
            print(f"   ⚠️  Aucun tableau structuré détecté, extraction du texte brut...")
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()

                    if page_text.strip():
                        table_type = self._identify_table_type_simple(page_text)
                        self.tables_data.append({
                            'page': page_num + 1,
                            'table_num': 1,
                            'type': table_type,
                            'content': page_text,
                            'raw_text': page_text
                        })

        print(f"✅ {len(self.tables_data)} section(s) extraite(s)")
        return self.tables_data

    def _detect_tables_in_text(self, text):
        """Détecte les tableaux dans le texte basé sur des patterns"""
        tables = []
        lines = text.split('\n')

        current_table = []
        in_table = False

        for line in lines:
            # Détecter si la ligne ressemble à une ligne de tableau
            # (contient plusieurs espaces ou séparateurs)
            if self._looks_like_table_row(line):
                current_table.append(line)
                in_table = True
            elif in_table and current_table:
                # Fin du tableau
                if len(current_table) >= 2:  # Au moins 2 lignes
                    tables.append('\n'.join(current_table))
                current_table = []
                in_table = False

        # Ajouter le dernier tableau si présent
        if current_table and len(current_table) >= 2:
            tables.append('\n'.join(current_table))

        return tables if tables else [text]  # Retourner tout le texte si aucun tableau

    def _looks_like_table_row(self, line):
        """Vérifie si une ligne ressemble à une ligne de tableau"""
        if not line.strip():
            return False

        # Compte les nombres et séparateurs
        has_numbers = bool(re.search(r'\d', line))
        has_multiple_spaces = len(re.findall(r'\s{2,}', line)) >= 2
        has_separators = any(sep in line for sep in ['|', '\t'])

        return (has_numbers and has_multiple_spaces) or has_separators

    def _identify_table_type_simple(self, text):
        """Identifie automatiquement le type de contenu"""
        combined_text = text.lower()

        # Patterns de détection
        patterns = {
            "📊 COMPTE DE RÉSULTAT": [
                r"chiffre d'affaires", r"revenus?", r"ventes?",
                r"résultat net", r"bénéfice", r"ebitda", r"ebit",
                r"charges", r"produits"
            ],
            "💰 BILAN": [
                r"actif", r"passif", r"capitaux propres",
                r"immobilisations", r"trésorerie", r"dettes",
                r"créances"
            ],
            "💸 FLUX DE TRÉSORERIE": [
                r"flux de trésorerie", r"cash.?flow",
                r"variation de trésorerie", r"activités opérationnelles",
                r"investissement", r"financement"
            ],
            "📈 RATIOS FINANCIERS": [
                r"ratio", r"marge", r"rentabilité",
                r"liquidité", r"solvabilité", r"%"
            ],
            "📅 DONNÉES TEMPORELLES": [
                r"\d{4}", r"20\d{2}", r"trimestre",
                r"année", r"période", r"exercice"
            ]
        }

        # Détecter le type
        scores = {}
        for table_type, keywords in patterns.items():
            score = 0
            for keyword in keywords:
                if re.search(keyword, combined_text):
                    score += 1
            scores[table_type] = score

        # Retourner le type avec le score le plus élevé
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        else:
            return "📋 TABLEAU GÉNÉRAL"

    def format_output(self):
        """Formate les résultats pour affichage"""
        if not self.tables_data:
            return "Aucun tableau trouvé dans le PDF"

        output_lines = []
        output_lines.append("=" * 100)
        output_lines.append(f"📄 EXTRACTION DE TABLEAUX PDF - {Path(self.file_path).name}")
        output_lines.append("=" * 100)
        output_lines.append(f"\n✅ {len(self.tables_data)} tableau(x) extrait(s)\n")

        for idx, table_info in enumerate(self.tables_data, 1):
            output_lines.append("-" * 100)
            output_lines.append(f"\n{table_info['type']}")
            output_lines.append(f"📍 Page {table_info['page']} | Tableau {table_info['table_num']}")
            lines_count = len(table_info.get('content', '').split('\n'))
            output_lines.append(f"📏 Lignes: {lines_count}")
            output_lines.append("")

            # Afficher le contenu
            content = table_info.get('content', '')
            if content:
                output_lines.append(content)
            else:
                output_lines.append("(Contenu vide)")

            output_lines.append("")

        output_lines.append("=" * 100)

        return "\n".join(output_lines)


class PDFExtractorGUI:
    """Interface graphique pour l'extracteur de tableaux PDF"""

    def __init__(self, root):
        self.root = root
        self.root.title("Extracteur de Tableaux PDF - Sans IA")
        self.root.geometry("1000x700")

        self.extractor = PDFTableExtractor()
        self.file_path = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        """Crée l'interface graphique"""

        # Titre
        title_frame = tk.Frame(self.root, bg="#2c3e50", pady=15)
        title_frame.pack(fill=tk.X)

        title_label = tk.Label(
            title_frame,
            text="📊 Extracteur de Tableaux PDF",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack()

        subtitle_label = tk.Label(
            title_frame,
            text="Extraction directe sans IA - Pas de perte de données",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        subtitle_label.pack()

        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Section fichier
        file_frame = tk.LabelFrame(
            main_frame,
            text="📄 Fichier PDF à analyser",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        file_frame.pack(fill=tk.X, pady=(0, 15))

        file_entry = tk.Entry(
            file_frame,
            textvariable=self.file_path,
            font=("Arial", 10),
            state="readonly"
        )
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        browse_btn = tk.Button(
            file_frame,
            text="📁 Sélectionner PDF...",
            command=self.browse_file,
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            padx=20,
            pady=5
        )
        browse_btn.pack(side=tk.LEFT)

        # Boutons d'action
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 15))

        extract_btn = tk.Button(
            button_frame,
            text="🚀 Extraire les Tableaux",
            command=self.extract_tables,
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            padx=30,
            pady=10
        )
        extract_btn.pack(side=tk.LEFT, padx=(0, 10))

        save_btn = tk.Button(
            button_frame,
            text="💾 Sauvegarder",
            command=self.save_results,
            font=("Arial", 12, "bold"),
            bg="#f39c12",
            fg="white",
            cursor="hand2",
            padx=30,
            pady=10
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 10))

        export_excel_btn = tk.Button(
            button_frame,
            text="📊 Exporter Excel",
            command=self.export_excel,
            font=("Arial", 12, "bold"),
            bg="#9b59b6",
            fg="white",
            cursor="hand2",
            padx=30,
            pady=10
        )
        export_excel_btn.pack(side=tk.LEFT, padx=(0, 10))

        clear_btn = tk.Button(
            button_frame,
            text="🗑️ Effacer",
            command=self.clear_results,
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            padx=30,
            pady=10
        )
        clear_btn.pack(side=tk.LEFT)

        # Zone de résultats
        results_frame = tk.LabelFrame(
            main_frame,
            text="📊 Tableaux extraits",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        results_frame.pack(fill=tk.BOTH, expand=True)

        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            font=("Courier", 9),
            wrap=tk.WORD,
            bg="#f8f9fa"
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # Barre de statut
        self.status_var = tk.StringVar(value="Prêt - Sélectionnez un fichier PDF")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Arial", 9),
            bg="#ecf0f1",
            anchor=tk.W,
            padx=10,
            pady=5
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def browse_file(self):
        """Ouvre le sélecteur de fichier"""
        filename = filedialog.askopenfilename(
            title="Sélectionnez un fichier PDF",
            filetypes=[
                ("Fichiers PDF", "*.pdf"),
                ("Tous les fichiers", "*.*")
            ]
        )

        if filename:
            self.file_path.set(filename)
            self.status_var.set(f"Fichier sélectionné: {Path(filename).name}")

    def extract_tables(self):
        """Extrait les tableaux du PDF"""
        if not self.file_path.get():
            messagebox.showwarning("Attention", "Veuillez sélectionner un fichier PDF")
            return

        try:
            self.status_var.set("⏳ Extraction en cours...")
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "⏳ Extraction des tableaux en cours...\n")
            self.root.update()

            # Extraire les tableaux
            self.extractor.extract_tables(self.file_path.get())

            # Afficher les résultats
            output = self.extractor.format_output()
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, output)

            self.status_var.set(f"✅ {len(self.extractor.tables_data)} tableau(x) extrait(s)")

        except Exception as e:
            error_msg = f"❌ Erreur lors de l'extraction:\n{str(e)}"
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, error_msg)
            self.status_var.set("❌ Erreur lors de l'extraction")
            messagebox.showerror("Erreur", str(e))

    def save_results(self):
        """Sauvegarde les résultats en fichier texte"""
        results = self.results_text.get(1.0, tk.END).strip()

        if not results or results.startswith("⏳"):
            messagebox.showwarning("Attention", "Aucun résultat à sauvegarder")
            return

        filename = filedialog.asksaveasfilename(
            title="Sauvegarder les résultats",
            defaultextension=".txt",
            filetypes=[
                ("Fichier texte", "*.txt"),
                ("Tous les fichiers", "*.*")
            ]
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(results)
                messagebox.showinfo("Succès", f"Résultats sauvegardés dans:\n{filename}")
                self.status_var.set(f"💾 Sauvegardé: {Path(filename).name}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder:\n{str(e)}")

    def export_excel(self):
        """Exporte les tableaux en fichier Excel (si pandas disponible)"""
        if not self.extractor.tables_data:
            messagebox.showwarning("Attention", "Aucune donnée à exporter")
            return

        if not PANDAS_AVAILABLE:
            messagebox.showwarning(
                "Module manquant",
                "Le module pandas n'est pas installé.\nUtilisez 'Sauvegarder' pour exporter en texte."
            )
            return

        filename = filedialog.asksaveasfilename(
            title="Exporter en CSV",
            defaultextension=".csv",
            filetypes=[
                ("Fichier CSV", "*.csv"),
                ("Fichier texte", "*.txt"),
                ("Tous les fichiers", "*.*")
            ]
        )

        if filename:
            try:
                all_content = []
                for table_info in self.extractor.tables_data:
                    all_content.append(f"\n--- Page {table_info['page']} - {table_info['type']} ---\n")
                    all_content.append(table_info.get('content', ''))
                    all_content.append("\n")

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(all_content))

                messagebox.showinfo(
                    "Succès",
                    f"Données exportées dans:\n{filename}"
                )
                self.status_var.set(f"📊 Exporté: {Path(filename).name}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'exporter:\n{str(e)}")

    def clear_results(self):
        """Efface les résultats"""
        self.results_text.delete(1.0, tk.END)
        self.extractor.tables_data = []
        self.status_var.set("Résultats effacés")


def main():
    """Lance l'application"""
    root = tk.Tk()
    app = PDFExtractorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
