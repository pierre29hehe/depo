#!/usr/bin/env python3
"""
Interface graphique pour l'analyseur de rapports financiers
Permet de sélectionner facilement les fichiers à analyser
"""

import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
import threading
import os
import sys
from pathlib import Path

# Importer l'analyseur
try:
    from financial_analyzer import FinancialReportAnalyzer, format_output
except ImportError:
    print("Erreur: Impossible d'importer financial_analyzer.py")
    sys.exit(1)


class FinancialAnalyzerGUI:
    """Interface graphique pour l'analyseur financier"""

    def __init__(self, root):
        self.root = root
        self.root.title("Analyseur de Rapports Financiers avec IA")
        self.root.geometry("900x700")

        # Variables
        self.file_path = tk.StringVar()
        self.backend_var = tk.StringVar(value="ollama")
        self.model_var = tk.StringVar(value="mistral:7b-instruct")
        self.calculations_var = tk.StringVar(value="all")
        self.analyzing = False

        # Créer l'interface
        self.create_widgets()

        # Charger les modèles disponibles
        self.load_available_models()

    def create_widgets(self):
        """Crée tous les widgets de l'interface"""

        # Titre
        title_frame = tk.Frame(self.root, bg="#2c3e50", pady=15)
        title_frame.pack(fill=tk.X)

        title_label = tk.Label(
            title_frame,
            text="📊 Analyseur de Rapports Financiers",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack()

        subtitle_label = tk.Label(
            title_frame,
            text="Analyse intelligente avec IA locale ou cloud",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        subtitle_label.pack()

        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Section 1: Sélection du fichier
        file_frame = tk.LabelFrame(main_frame, text="📄 Fichier à analyser", font=("Arial", 11, "bold"), padx=10, pady=10)
        file_frame.pack(fill=tk.X, pady=(0, 15))

        file_entry = tk.Entry(file_frame, textvariable=self.file_path, font=("Arial", 10), state="readonly")
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        browse_btn = tk.Button(
            file_frame,
            text="📁 Parcourir...",
            command=self.browse_file,
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            padx=20,
            pady=5
        )
        browse_btn.pack(side=tk.LEFT)

        # Section 2: Configuration
        config_frame = tk.LabelFrame(main_frame, text="⚙️ Configuration", font=("Arial", 11, "bold"), padx=10, pady=10)
        config_frame.pack(fill=tk.X, pady=(0, 15))

        # Backend
        backend_frame = tk.Frame(config_frame)
        backend_frame.pack(fill=tk.X, pady=5)

        tk.Label(backend_frame, text="Backend IA:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))

        backends = [
            ("Ollama (Local - Gratuit)", "ollama"),
            ("Open Interpreter (Local + Code)", "open-interpreter"),
            ("Claude AI (Cloud)", "anthropic")
        ]

        for text, value in backends:
            rb = tk.Radiobutton(
                backend_frame,
                text=text,
                variable=self.backend_var,
                value=value,
                font=("Arial", 9),
                command=self.on_backend_change
            )
            rb.pack(side=tk.LEFT, padx=10)

        # Modèle
        model_frame = tk.Frame(config_frame)
        model_frame.pack(fill=tk.X, pady=5)

        tk.Label(model_frame, text="Modèle:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))

        self.model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            font=("Arial", 10),
            state="readonly",
            width=30
        )
        self.model_combo.pack(side=tk.LEFT, padx=(0, 10))

        # Type de calculs
        calc_frame = tk.Frame(config_frame)
        calc_frame.pack(fill=tk.X, pady=5)

        tk.Label(calc_frame, text="Calculs:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))

        calc_combo = ttk.Combobox(
            calc_frame,
            textvariable=self.calculations_var,
            font=("Arial", 10),
            state="readonly",
            values=["all - Analyse complète", "ratios - Ratios financiers", "margins - Marges", "growth - Croissance"],
            width=30
        )
        calc_combo.current(0)
        calc_combo.pack(side=tk.LEFT)

        # Section 3: Boutons d'action
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 15))

        self.analyze_btn = tk.Button(
            button_frame,
            text="🚀 Analyser le Rapport",
            command=self.analyze_file,
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            padx=30,
            pady=10
        )
        self.analyze_btn.pack(side=tk.LEFT, padx=(0, 10))

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

        # Section 4: Résultats
        results_frame = tk.LabelFrame(main_frame, text="📊 Résultats de l'analyse", font=("Arial", 11, "bold"), padx=10, pady=10)
        results_frame.pack(fill=tk.BOTH, expand=True)

        # Zone de texte avec scrollbar
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            font=("Courier", 9),
            wrap=tk.WORD,
            bg="#f8f9fa"
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # Barre de statut
        self.status_var = tk.StringVar(value="Prêt")
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

    def load_available_models(self):
        """Charge la liste des modèles disponibles"""
        try:
            from financial_analyzer import OllamaBackend
            backend = OllamaBackend()
            models = backend.list_models()

            if models:
                self.model_combo['values'] = models
                if models:
                    self.model_var.set(models[0])
            else:
                self.model_combo['values'] = [
                    "mistral:7b-instruct",
                    "llama3.1:8b",
                    "qwen2.5-coder:7b",
                    "deepseek-r1:8b",
                    "qwen2.5:7b"
                ]
        except Exception as e:
            print(f"Erreur lors du chargement des modèles: {e}")
            self.model_combo['values'] = ["mistral:7b-instruct"]

    def on_backend_change(self):
        """Appelé quand le backend change"""
        backend = self.backend_var.get()

        if backend == "anthropic":
            self.model_combo['values'] = [
                "claude-3-5-sonnet-20241022",
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229"
            ]
            self.model_var.set("claude-3-5-sonnet-20241022")
        else:
            self.load_available_models()

    def browse_file(self):
        """Ouvre une fenêtre de dialogue pour sélectionner un fichier"""
        filetypes = [
            ("Tous les fichiers supportés", "*.pdf *.xlsx *.xls *.csv *.txt"),
            ("Fichiers PDF", "*.pdf"),
            ("Fichiers Excel", "*.xlsx *.xls"),
            ("Fichiers CSV", "*.csv"),
            ("Fichiers texte", "*.txt"),
            ("Tous les fichiers", "*.*")
        ]

        filename = filedialog.askopenfilename(
            title="Sélectionnez un rapport financier",
            filetypes=filetypes
        )

        if filename:
            self.file_path.set(filename)
            self.status_var.set(f"Fichier sélectionné: {Path(filename).name}")

    def analyze_file(self):
        """Lance l'analyse du fichier"""
        if not self.file_path.get():
            messagebox.showwarning("Attention", "Veuillez sélectionner un fichier à analyser")
            return

        if self.analyzing:
            messagebox.showinfo("Info", "Une analyse est déjà en cours...")
            return

        # Lancer l'analyse dans un thread séparé
        self.analyzing = True
        self.analyze_btn.config(state=tk.DISABLED, text="⏳ Analyse en cours...")
        self.status_var.set("Analyse en cours...")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "⏳ Analyse en cours, veuillez patienter...\n\n")

        thread = threading.Thread(target=self._analyze_thread)
        thread.daemon = True
        thread.start()

    def _analyze_thread(self):
        """Thread d'analyse"""
        try:
            # Extraire le type de calculs
            calc_type = self.calculations_var.get().split(" - ")[0]

            # Créer l'analyseur
            analyzer = FinancialReportAnalyzer(
                backend=self.backend_var.get(),
                model=self.model_var.get()
            )

            # Analyser
            results = analyzer.process_report(
                self.file_path.get(),
                calculations=calc_type
            )

            # Formater les résultats
            output = format_output(results, "text")

            # Afficher les résultats dans l'interface
            self.root.after(0, self._display_results, output, results.get("success", False))

        except Exception as e:
            error_msg = f"❌ Erreur lors de l'analyse:\n{str(e)}"
            self.root.after(0, self._display_results, error_msg, False)

    def _display_results(self, output, success):
        """Affiche les résultats dans l'interface"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, output)

        if success:
            self.status_var.set("✅ Analyse terminée avec succès")
        else:
            self.status_var.set("❌ Erreur lors de l'analyse")

        self.analyze_btn.config(state=tk.NORMAL, text="🚀 Analyser le Rapport")
        self.analyzing = False

    def save_results(self):
        """Sauvegarde les résultats dans un fichier"""
        results = self.results_text.get(1.0, tk.END).strip()

        if not results or results == "⏳ Analyse en cours, veuillez patienter...":
            messagebox.showwarning("Attention", "Aucun résultat à sauvegarder")
            return

        filename = filedialog.asksaveasfilename(
            title="Sauvegarder l'analyse",
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
                self.status_var.set(f"Sauvegardé: {Path(filename).name}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder:\n{str(e)}")

    def clear_results(self):
        """Efface les résultats"""
        self.results_text.delete(1.0, tk.END)
        self.status_var.set("Résultats effacés")


def main():
    """Lance l'interface graphique"""
    root = tk.Tk()
    app = FinancialAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
