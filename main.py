# -*- coding: utf-8 -*-
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from data import DOMAINS, build_questionnaire
from reports import compute, generate_internal_report, generate_opinion_report, OPINION_LABEL

CHOICES = ["Oui", "Partiellement", "Non", "N/A"]
BLUE = "#1F3864"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AuditPro - Audit interne et opinion sur les comptes")
        self.geometry("1050x720")
        self.minsize(900, 600)
        self.info = {}
        self.sections = []
        self.page = 0
        self.vars = {}
        self.show_start()

    # ---------- utilitaires ----------
    def clear(self):
        self.unbind_all("<MouseWheel>")
        for w in self.winfo_children():
            w.destroy()

    # ---------- écran de démarrage ----------
    def show_start(self):
        self.clear()
        f = ttk.Frame(self, padding=40)
        f.pack(fill="both", expand=True)
        tk.Label(f, text="AuditPro", font=("Segoe UI", 28, "bold"), fg=BLUE).pack(anchor="w")
        tk.Label(f, text="Questionnaire d'audit, rapport d'audit interne et rapport d'opinion sur les comptes",
                 font=("Segoe UI", 11)).pack(anchor="w", pady=(0, 25))

        self.e_entity = self._field(f, "Nom de l'entité auditée")
        self.e_period = self._field(f, "Exercice / période (ex. exercice clos le 31/12/2025)")
        self.e_auditor = self._field(f, "Nom de l'auditeur / cabinet")
        tk.Label(f, text="Domaine d'activité", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 2))
        self.c_domain = ttk.Combobox(f, values=DOMAINS, state="readonly", width=40)
        self.c_domain.current(0)
        self.c_domain.pack(anchor="w")

        b = ttk.Frame(f)
        b.pack(anchor="w", pady=30)
        ttk.Button(b, text="Démarrer l'audit", command=self.start).pack(side="left", padx=(0, 10))
        ttk.Button(b, text="Reprendre une sauvegarde", command=self.load).pack(side="left")

    def _field(self, parent, label):
        tk.Label(parent, text=label, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 2))
        e = ttk.Entry(parent, width=60)
        e.pack(anchor="w")
        return e

    def start(self):
        info = {"entity": self.e_entity.get().strip(), "period": self.e_period.get().strip(),
                "auditor": self.e_auditor.get().strip(), "domain": self.c_domain.get()}
        if not all(info.values()):
            messagebox.showwarning("Champs manquants", "Merci de renseigner tous les champs.")
            return
        self.info = info
        self.sections = build_questionnaire(info["domain"])
        self.page = 0
        self.show_page()

    # ---------- sauvegarde / reprise ----------
    def save(self):
        self.collect()
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Sauvegarde AuditPro", "*.json")],
                                            initialfile="audit_en_cours.json")
        if not path:
            return
        data = {"info": self.info, "page": self.page,
                "answers": {q["id"]: [q["answer"], q["comment"]] for _, qs in self.sections for q in qs}}
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        messagebox.showinfo("Sauvegarde", "Audit sauvegardé.")

    def load(self):
        path = filedialog.askopenfilename(filetypes=[("Sauvegarde AuditPro", "*.json")])
        if not path:
            return
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
            self.info = data["info"]
            self.sections = build_questionnaire(self.info["domain"])
            for _, qs in self.sections:
                for q in qs:
                    a, c = data["answers"].get(q["id"], ["", ""])
                    q["answer"], q["comment"] = a, c
            self.page = min(data.get("page", 0), len(self.sections) - 1)
            self.show_page()
        except Exception as e:
            messagebox.showerror("Erreur", f"Fichier invalide : {e}")

    # ---------- pages du questionnaire ----------
    def collect(self):
        for _, qs in self.sections:
            for q in qs:
                if q["id"] in self.vars:
                    q["answer"] = self.vars[q["id"]][0].get()
                    q["comment"] = self.vars[q["id"]][1].get().strip()

    def show_page(self):
        self.clear()
        self.vars = {}
        name, qs = self.sections[self.page]
        total = len(self.sections)

        head = tk.Frame(self, bg=BLUE)
        head.pack(fill="x")
        tk.Label(head, text=f"{self.info['entity']}  |  {self.info['domain']}", bg=BLUE, fg="white",
                 font=("Segoe UI", 10)).pack(anchor="w", padx=15, pady=(8, 0))
        tk.Label(head, text=name, bg=BLUE, fg="white", font=("Segoe UI", 15, "bold")).pack(anchor="w", padx=15)
        pb = ttk.Progressbar(head, maximum=total, value=self.page + 1)
        pb.pack(fill="x", padx=15, pady=8)
        tk.Label(head, text=f"Section {self.page + 1} / {total}", bg=BLUE, fg="white").pack(anchor="e", padx=15, pady=(0, 6))

        body = ttk.Frame(self)
        body.pack(fill="both", expand=True)
        canvas = tk.Canvas(body, highlightthickness=0)
        sb = ttk.Scrollbar(body, orient="vertical", command=canvas.yview)
        inner = ttk.Frame(canvas)
        win = canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfigure(win, width=e.width))
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-e.delta / 120), "units"))

        for q in qs:
            box = tk.LabelFrame(inner, text=q["id"] + ("  (critique)" if q["weight"] == 3 else ""),
                                font=("Segoe UI", 8), padx=10, pady=6)
            box.pack(fill="x", padx=15, pady=6)
            tk.Label(box, text=q["text"], font=("Segoe UI", 10, "bold"), wraplength=900, justify="left").pack(anchor="w")
            tk.Label(box, text="Bonne pratique : " + q["practice"], fg="#2E7D32", font=("Segoe UI", 9, "italic"),
                     wraplength=900, justify="left").pack(anchor="w", pady=(2, 4))
            av, cv = tk.StringVar(value=q["answer"]), tk.StringVar(value=q["comment"])
            self.vars[q["id"]] = (av, cv)
            row = ttk.Frame(box)
            row.pack(anchor="w", fill="x")
            for c in CHOICES:
                ttk.Radiobutton(row, text=c, value=c, variable=av).pack(side="left", padx=(0, 14))
            tk.Label(row, text="Commentaire :").pack(side="left", padx=(20, 4))
            ttk.Entry(row, textvariable=cv, width=45).pack(side="left", fill="x", expand=True)

        nav = ttk.Frame(self, padding=10)
        nav.pack(fill="x")
        ttk.Button(nav, text="Sauvegarder", command=self.save).pack(side="left")
        if self.page < total - 1:
            ttk.Button(nav, text="Suivant ▶", command=lambda: self.go(1)).pack(side="right")
        else:
            ttk.Button(nav, text="Terminer et générer les rapports", command=self.finish).pack(side="right")
        if self.page > 0:
            ttk.Button(nav, text="◀ Précédent", command=lambda: self.go(-1)).pack(side="right", padx=8)

    def go(self, d):
        self.collect()
        self.page += d
        self.show_page()

    # ---------- génération ----------
    def finish(self):
        self.collect()
        missing = [q["id"] for _, qs in self.sections for q in qs if not q["answer"]]
        if missing:
            if not messagebox.askyesno("Questions sans réponse",
                                       f"{len(missing)} question(s) sans réponse (ex. {missing[0]}). "
                                       "Elles seront ignorées. Continuer ?"):
                return
        folder = filedialog.askdirectory(title="Dossier d'enregistrement des rapports")
        if not folder:
            return
        try:
            res = compute(self.sections)
            p1 = generate_internal_report(self.info, self.sections, res, folder)
            p2 = generate_opinion_report(self.info, self.sections, res, folder)
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec de la génération : {e}")
            return
        messagebox.showinfo("Rapports générés",
                            f"Score global : {res['global']} %\nOpinion : {OPINION_LABEL[res['opinion']]}\n\n"
                            f"{os.path.basename(p1)}\n{os.path.basename(p2)}")
        try:
            os.startfile(folder)
        except Exception:
            pass


if __name__ == "__main__":
    App().mainloop()
