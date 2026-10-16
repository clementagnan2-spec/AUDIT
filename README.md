# AuditPro

Logiciel d'audit : choix du domaine (Banque, Négoce, Usine, ONG humanitaire, ONG agricole) -> questionnaire QCM avec bonnes pratiques
-> génération de 2 rapports Word : audit interne + opinion sur la sincérité et l'image fidèle des comptes.

## Obtenir le .exe via GitHub
1. Créez un dépôt GitHub et envoyez-y tout ce dossier (y compris `.github/`).
2. Onglet **Actions** -> workflow *Build AuditPro EXE* -> une fois terminé, téléchargez l'artefact `AuditPro-windows` (AuditPro.exe).
3. Pour une release publique : `git tag v1.0.0 && git push --tags` (l'exe est joint à la release).

## Lancer en local
    pip install -r requirements.txt
    python main.py

## Personnaliser
Les questions sont dans `data.py` (texte, bonne pratique, poids 1-3, drapeau C/L). Les règles d'opinion sont dans `reports.py` (`compute`).
