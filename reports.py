# -*- coding: utf-8 -*-
import os
from datetime import date
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

VALUES = {"Oui": 1.0, "Partiellement": 0.5, "Non": 0.0}


def _score(qs):
    num = den = 0.0
    for q in qs:
        v = VALUES.get(q["answer"])
        if v is None:
            continue
        num += q["weight"] * v
        den += q["weight"]
    return None if den == 0 else round(100 * num / den, 1)


def risk_level(q):
    sev = q["weight"] * (1.0 if q["answer"] == "Non" else 0.5)
    return "Élevé" if sev >= 3 else "Moyen" if sev >= 1.5 else "Faible"


def maturity(score):
    if score is None:
        return "Non évaluable"
    if score >= 85:
        return "Satisfaisant"
    if score >= 70:
        return "Acceptable, améliorations nécessaires"
    if score >= 50:
        return "Insuffisant"
    return "Critique"


def compute(sections):
    allq = [q for _, qs in sections for q in qs]
    answered = [q for q in allq if q["answer"] in VALUES]
    acct = [q for q in allq if q["flag"] == "C"]
    findings = [dict(q, section=s, risk=risk_level(q))
                for s, qs in sections for q in qs if q["answer"] in ("Non", "Partiellement")]
    order = {"Élevé": 0, "Moyen": 1, "Faible": 2}
    findings.sort(key=lambda f: (order[f["risk"]], f["id"]))
    limitation = any(q["flag"] == "L" and q["answer"] == "Non" for q in allq)
    critical = [q for q in acct if q["weight"] == 3 and q["answer"] == "Non"]
    acct_score = _score(acct)

    if limitation or acct_score is None:
        opinion = "impossibilite"
    elif acct_score >= 85 and not critical:
        opinion = "sans_reserve"
    elif acct_score >= 70 and len(critical) <= 2:
        opinion = "reserve"
    elif acct_score >= 40:
        opinion = "defavorable"
    else:
        opinion = "impossibilite"

    return {
        "global": _score(allq), "accounting": acct_score,
        "by_section": [(s, _score(qs)) for s, qs in sections],
        "findings": findings, "limitation": limitation, "critical": critical,
        "opinion": opinion, "n_total": len(allq), "n_answered": len(answered),
        "n_na": sum(1 for q in allq if q["answer"] == "N/A"),
        "n_ok": sum(1 for q in allq if q["answer"] == "Oui"),
    }


OPINION_LABEL = {
    "sans_reserve": "Opinion favorable sans réserve",
    "reserve": "Opinion favorable avec réserve(s)",
    "defavorable": "Opinion défavorable",
    "impossibilite": "Impossibilité d'exprimer une opinion",
}

# ---------- utilitaires docx ----------

def _shade(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def _table(doc, headers, rows, widths=None, risk_col=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = ""
        r = c.paragraphs[0].add_run(h)
        r.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)
        _shade(c, "1F3864")
    colors = {"Élevé": "F8CBAD", "Moyen": "FFE699", "Faible": "C6E0B4"}
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            run = cells[i].paragraphs[0].add_run(str(v))
            run.font.size = Pt(9)
            if risk_col is not None and i == risk_col and v in colors:
                _shade(cells[i], colors[v])
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
    return t


def _base_doc(title, info, subtitle):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(title)
    r.bold = True
    r.font.size = Pt(20)
    r.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(subtitle).italic = True
    _table(doc, ["Élément", "Détail"], [
        ("Entité auditée", info["entity"]),
        ("Secteur d'activité", info["domain"]),
        ("Exercice / période", info["period"]),
        ("Auditeur", info["auditor"]),
        ("Date du rapport", date.today().strftime("%d/%m/%Y")),
    ], widths=[5, 12])
    return doc


# ---------- rapport d'audit interne ----------

def generate_internal_report(info, sections, res, folder):
    doc = _base_doc("RAPPORT D'AUDIT INTERNE", info, "Évaluation du dispositif de contrôle interne")

    doc.add_heading("1. Objectifs et méthodologie", 1)
    doc.add_paragraph(
        "La mission a consisté à évaluer le dispositif de contrôle interne de l'entité à partir d'un questionnaire "
        f"structuré de {res['n_total']} points de contrôle couvrant les principales procédures du secteur « {info['domain']} ». "
        "Chaque réponse (Oui / Partiellement / Non / N/A) est comparée à la bonne pratique de référence. "
        "Les points sont pondérés selon leur criticité (1 à 3). Score = Σ(poids × note) / Σ poids, avec Oui = 1, Partiellement = 0,5, Non = 0 ; "
        "les points N/A sont exclus du calcul.")

    doc.add_heading("2. Synthèse générale", 1)
    doc.add_paragraph(
        f"Score global de maîtrise : {res['global']} % — niveau : {maturity(res['global'])}.\n"
        f"Points contrôlés : {res['n_answered']} / {res['n_total']} (dont {res['n_ok']} conformes, "
        f"{len(res['findings'])} écarts, {res['n_na']} non applicables).")
    _table(doc, ["Domaine de contrôle", "Score", "Niveau de maîtrise"],
           [(s, "-" if sc is None else f"{sc} %", maturity(sc)) for s, sc in res["by_section"]],
           widths=[8.5, 2.5, 6])

    doc.add_heading("3. Constats et recommandations", 1)
    if not res["findings"]:
        doc.add_paragraph("Aucun écart n'a été relevé.")
    else:
        rows = [(f["id"], f["section"].split(". ", 1)[-1], f["text"], f["answer"], f["risk"],
                 f["practice"], f["comment"] or "-") for f in res["findings"]]
        _table(doc, ["Réf.", "Domaine", "Point de contrôle", "Réponse", "Risque",
                     "Recommandation (bonne pratique)", "Commentaire"],
               rows, widths=[1.2, 2.2, 4.3, 1.8, 1.3, 4.2, 2.3], risk_col=4)

    doc.add_heading("4. Plan d'actions priorisé", 1)
    delays = {"Élevé": "Sous 1 mois", "Moyen": "Sous 3 mois", "Faible": "Sous 6 mois"}
    if res["findings"]:
        _table(doc, ["Priorité", "Réf.", "Action à mener", "Délai", "Responsable"],
               [(f["risk"], f["id"], f["practice"], delays[f["risk"]], "À désigner") for f in res["findings"]],
               widths=[1.8, 1.4, 9, 2.4, 2.8], risk_col=0)

    doc.add_heading("5. Conclusion", 1)
    nb_h = sum(1 for f in res["findings"] if f["risk"] == "Élevé")
    doc.add_paragraph(
        f"Le dispositif de contrôle interne est jugé « {maturity(res['global']).lower()} ». "
        f"{nb_h} constat(s) à risque élevé nécessitent une action corrective prioritaire. "
        "Nous recommandons un suivi trimestriel de la mise en œuvre du plan d'actions par la direction.")
    doc.add_paragraph("\nNom et signature de l'auditeur : ______________________________")
    p = doc.add_paragraph("Rapport généré avec l'aide d'un outil de questionnaire ; il repose sur les réponses déclarées et "
                          "doit être complété par des tests et vérifications documentaires de l'auditeur.")
    p.runs[0].italic = True
    p.runs[0].font.size = Pt(8)

    path = os.path.join(folder, f"Rapport_Audit_Interne_{_safe(info['entity'])}.docx")
    doc.save(path)
    return path


# ---------- rapport d'opinion ----------

def generate_opinion_report(info, sections, res, folder):
    op = res["opinion"]
    ent, per = info["entity"], info["period"]
    doc = _base_doc("RAPPORT SUR LA SINCÉRITÉ ET L'IMAGE FIDÈLE DES COMPTES", info,
                    "Rapport de l'auditeur sur les états financiers — PROJET")

    doc.add_heading("Opinion", 1)
    if op == "sans_reserve":
        txt = (f"Nous avons effectué l'audit des états financiers de {ent} pour la période {per}. "
               "Selon notre opinion, les états financiers sont réguliers et sincères et donnent une image fidèle du résultat "
               "des opérations de l'exercice, ainsi que de la situation financière et du patrimoine de l'entité à la fin de cet exercice, "
               "conformément au référentiel comptable applicable.")
    elif op == "reserve":
        txt = (f"Nous avons effectué l'audit des états financiers de {ent} pour la période {per}. "
               "Sous réserve des points décrits dans la section « Fondement de l'opinion avec réserve(s) », les états financiers sont "
               "réguliers et sincères et donnent une image fidèle du résultat des opérations de l'exercice, ainsi que de la situation "
               "financière et du patrimoine de l'entité à la fin de cet exercice, conformément au référentiel comptable applicable.")
    elif op == "defavorable":
        txt = (f"Nous avons effectué l'audit des états financiers de {ent} pour la période {per}. "
               "Compte tenu de l'importance des points décrits dans la section « Fondement de l'opinion défavorable », les états financiers "
               "ne sont pas réguliers et sincères et ne donnent pas une image fidèle du résultat, de la situation financière et du "
               "patrimoine de l'entité conformément au référentiel comptable applicable.")
    else:
        txt = (f"Nous avons été missionnés pour auditer les états financiers de {ent} pour la période {per}. "
               "Nous n'avons pas été en mesure de recueillir des éléments probants suffisants et appropriés pour fonder une opinion. "
               "En conséquence, nous n'exprimons pas d'opinion sur la régularité, la sincérité et l'image fidèle de ces états financiers.")
    doc.add_paragraph(txt)
    p = doc.add_paragraph()
    r = p.add_run(f"Type d'opinion : {OPINION_LABEL[op]}")
    r.bold = True

    doc.add_heading("Fondement de l'opinion", 1)
    doc.add_paragraph(
        "Notre évaluation s'appuie sur l'examen du contrôle interne et des procédures comptables, selon un questionnaire structuré "
        "comparé aux bonnes pratiques. "
        f"Le score de fiabilité des processus à impact comptable ressort à {res['accounting']} % "
        f"(score global de contrôle interne : {res['global']} %).")
    if res["limitation"]:
        doc.add_paragraph("Limitation de l'étendue des travaux : l'accès à l'ensemble des documents, registres et interlocuteurs "
                          "demandés n'a pas été donné, ce qui nous a empêché de mettre en œuvre toutes les procédures nécessaires.")
    acct_findings = [f for f in res["findings"] if f["flag"] == "C"]
    if op != "sans_reserve" and acct_findings:
        doc.add_paragraph("Points ayant une incidence sur les comptes :")
        for f in acct_findings:
            if f["risk"] in ("Élevé", "Moyen"):
                doc.add_paragraph(f"[{f['id']}] {f['text']} — Réponse : {f['answer']}. "
                                  f"Risque : {f['risk']}." + (f" Commentaire : {f['comment']}" if f["comment"] else ""),
                                  style="List Bullet")

    doc.add_heading("Responsabilités de la direction", 1)
    doc.add_paragraph(
        "La direction est responsable de l'établissement d'états financiers réguliers et sincères conformément au référentiel comptable, "
        "ainsi que du contrôle interne qu'elle estime nécessaire pour permettre l'établissement d'états financiers exempts d'anomalies "
        "significatives, que celles-ci résultent de fraudes ou d'erreurs. Il lui incombe d'évaluer la capacité de l'entité à poursuivre son exploitation.")

    doc.add_heading("Responsabilités de l'auditeur", 1)
    doc.add_paragraph(
        "Notre objectif est d'obtenir l'assurance raisonnable que les états financiers pris dans leur ensemble ne comportent pas "
        "d'anomalies significatives, et d'émettre un rapport contenant notre opinion. L'assurance raisonnable correspond à un niveau "
        "élevé d'assurance, sans toutefois garantir qu'un audit réalisé conformément aux normes professionnelles permettra "
        "de toujours détecter toute anomalie significative.")
    doc.add_paragraph("\nFait à ____________, le " + date.today().strftime("%d/%m/%Y"))
    doc.add_paragraph("Nom et signature de l'auditeur : ______________________________")

    doc.add_heading("Annexe — Règles de détermination de l'opinion (outil)", 1)
    for line in [
        "Sans réserve : score comptable ≥ 85 % et aucun point critique (poids 3, impact comptable) en réponse « Non ».",
        "Avec réserve(s) : score comptable ≥ 70 % et au plus 2 points critiques non conformes.",
        "Défavorable : score comptable entre 40 % et 70 %, ou plus de 2 points critiques non conformes.",
        "Impossibilité d'exprimer une opinion : limitation d'accès aux documents, ou score comptable < 40 %.",
    ]:
        doc.add_paragraph(line, style="List Bullet")
    p = doc.add_paragraph("PROJET d'opinion établi automatiquement à partir des réponses du questionnaire. Il doit être revu, complété par "
                          "des travaux d'audit des comptes (circularisation, contrôles de détail, inventaires) et validé par un professionnel "
                          "habilité avant toute diffusion. Il ne constitue pas un rapport de commissaire aux comptes.")
    p.runs[0].italic = True
    p.runs[0].font.size = Pt(8)

    path = os.path.join(folder, f"Rapport_Opinion_Comptes_{_safe(info['entity'])}.docx")
    doc.save(path)
    return path


def _safe(s):
    return "".join(c if c.isalnum() else "_" for c in s)[:40] or "entite"
