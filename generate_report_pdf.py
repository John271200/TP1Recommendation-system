from pathlib import Path
import textwrap


BASE_DIR = Path(__file__).parent
OUTPUT_PATH = BASE_DIR / "RAPPORT_TP1_AGBESSI_John_Ulrich.pdf"

PAGE_WIDTH = 595
PAGE_HEIGHT = 842
LEFT = 54
RIGHT = 54
TOP = 72
BOTTOM = 64
CONTENT_WIDTH = PAGE_WIDTH - LEFT - RIGHT

BLUE = "0.07 0.20 0.38"
LIGHT_BLUE = "0.88 0.93 0.98"
MID_BLUE = "0.16 0.36 0.61"
GRAY = "0.32 0.34 0.36"
LIGHT_GRAY = "0.94 0.95 0.96"
TEXT = "0.12 0.13 0.15"
WHITE = "1 1 1"


def esc(text):
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


class PdfBuilder:
    def __init__(self):
        self.pages = []
        self.current = []
        self.y = PAGE_HEIGHT - TOP

    def new_page(self):
        if self.current:
            self.pages.append(self.current)
        self.current = []
        self.y = PAGE_HEIGHT - TOP

    def ensure(self, height):
        if self.y - height < BOTTOM:
            self.new_page()

    def cmd(self, command):
        self.current.append(command)

    def rect(self, x, y, w, h, color, stroke=None):
        self.cmd(f"{color} rg")
        self.cmd(f"{x} {y} {w} {h} re f")
        if stroke:
            self.cmd(f"{stroke} RG")
            self.cmd(f"{x} {y} {w} {h} re S")

    def line(self, x1, y1, x2, y2, color=GRAY, width=0.8):
        self.cmd(f"{color} RG")
        self.cmd(f"{width} w")
        self.cmd(f"{x1} {y1} m {x2} {y2} l S")

    def text(self, x, y, text, size=11, font="F1", color=TEXT):
        self.cmd("BT")
        self.cmd(f"{color} rg")
        self.cmd(f"/{font} {size} Tf")
        self.cmd(f"{x} {y} Td ({esc(text)}) Tj")
        self.cmd("ET")

    def paragraph(self, text, size=10.5, font="F1", width_chars=88, leading=15, color=TEXT, gap=7):
        lines = []
        for part in text.split("\n"):
            if part.strip():
                lines.extend(textwrap.wrap(part, width=width_chars))
            else:
                lines.append("")
        self.ensure(len(lines) * leading + gap)
        for line in lines:
            self.text(LEFT, self.y, line, size=size, font=font, color=color)
            self.y -= leading
        self.y -= gap

    def heading(self, title, number=None):
        label = f"{number}. {title}" if number else title
        self.ensure(42)
        self.y -= 8
        self.text(LEFT, self.y, label, size=15, font="F2", color=BLUE)
        self.y -= 8
        self.line(LEFT, self.y, PAGE_WIDTH - RIGHT, self.y, MID_BLUE, 1.2)
        self.y -= 18

    def subheading(self, title):
        self.ensure(30)
        self.text(LEFT, self.y, title, size=12, font="F2", color=MID_BLUE)
        self.y -= 19

    def bullet(self, items):
        self.ensure(len(items) * 16 + 6)
        for item in items:
            wrapped = textwrap.wrap(item, width=82)
            self.text(LEFT + 6, self.y, "-", size=10.5, font="F2", color=MID_BLUE)
            self.text(LEFT + 20, self.y, wrapped[0], size=10.5)
            self.y -= 15
            for extra in wrapped[1:]:
                self.text(LEFT + 20, self.y, extra, size=10.5)
                self.y -= 15
        self.y -= 6

    def code_block(self, lines):
        height = len(lines) * 14 + 18
        self.ensure(height)
        y0 = self.y - height + 8
        self.rect(LEFT, y0, CONTENT_WIDTH, height, LIGHT_GRAY)
        self.line(LEFT, y0 + height, LEFT + CONTENT_WIDTH, y0 + height, "0.80 0.82 0.85", 0.7)
        self.y -= 20
        for line in lines:
            self.text(LEFT + 12, self.y, line, size=9, font="F3", color="0.10 0.10 0.10")
            self.y -= 14
        self.y -= 10

    def info_box(self, title, rows):
        height = 36 + len(rows) * 22
        self.ensure(height + 10)
        y0 = self.y - height
        self.rect(LEFT, y0, CONTENT_WIDTH, height, LIGHT_BLUE)
        self.rect(LEFT, y0 + height - 30, CONTENT_WIDTH, 30, BLUE)
        self.text(LEFT + 14, y0 + height - 20, title, size=12, font="F2", color=WHITE)
        y = y0 + height - 52
        for key, value in rows:
            self.text(LEFT + 14, y, key, size=10, font="F2", color=BLUE)
            self.text(LEFT + 135, y, value, size=10, font="F1", color=TEXT)
            y -= 22
        self.y = y0 - 18

    def table(self, headers, rows, col_widths):
        row_h = 24
        height = row_h * (len(rows) + 1)
        self.ensure(height + 12)
        y = self.y - row_h
        x = LEFT
        self.rect(LEFT, y, sum(col_widths), row_h, BLUE)
        for header, width in zip(headers, col_widths):
            self.text(x + 8, y + 8, header, size=9, font="F2", color=WHITE)
            x += width
        for row in rows:
            y -= row_h
            self.rect(LEFT, y, sum(col_widths), row_h, "0.98 0.99 1.00")
            x = LEFT
            for value, width in zip(row, col_widths):
                self.text(x + 8, y + 8, value, size=9)
                x += width
            self.line(LEFT, y, LEFT + sum(col_widths), y, "0.84 0.86 0.88", 0.5)
        self.y = y - 18

    def cover(self):
        self.current = []
        self.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, "0.98 0.99 1.00")
        self.rect(0, PAGE_HEIGHT - 210, PAGE_WIDTH, 210, BLUE)
        self.text(LEFT, 745, "IFRI-UAC", size=16, font="F2", color=WHITE)
        self.text(LEFT, 700, "Rapport de projet", size=26, font="F2", color=WHITE)
        self.text(LEFT, 664, "TP1 Big Data", size=19, font="F2", color=WHITE)
        self.text(LEFT, 632, "Recommendation system: Collaborative Filtering item-item top-N", size=13, font="F1", color=WHITE)
        self.rect(LEFT, 382, CONTENT_WIDTH, 178, WHITE)
        self.text(LEFT + 22, 525, "Informations etudiant", size=14, font="F2", color=BLUE)
        rows = [
            ("Nom et prenoms", "AGBESSI John Ulrich"),
            ("Filiere", "Genie logiciel"),
            ("Ecole", "IFRI-UAC"),
            ("Depot GitHub", "github.com/John271200/TP1Recommendation-system"),
            ("Application", "tp1recommendation-system.streamlit.app"),
        ]
        y = 493
        for key, value in rows:
            self.text(LEFT + 22, y, key + " :", size=10.5, font="F2", color=GRAY)
            self.text(LEFT + 150, y, value, size=10.5, color=TEXT)
            y -= 24
        self.text(LEFT, 96, "Projet realise dans le cadre du TP1 : Recommendation system avec Streamlit", size=10.5, color=GRAY)
        self.pages.append(self.current)
        self.current = []
        self.y = PAGE_HEIGHT - TOP

    def finish(self):
        if self.current:
            self.pages.append(self.current)
            self.current = []


def build_report():
    pdf = PdfBuilder()
    pdf.cover()

    pdf.heading("Resume")
    pdf.paragraph(
        "Ce rapport presente la conception et la realisation d'un systeme de recommandation top-N base sur le filtrage collaboratif item-item. "
        "Le systeme exploite les notes donnees par plusieurs utilisateurs a des films, calcule les similarites entre les items, puis recommande "
        "les films les plus pertinents pour un utilisateur cible."
    )
    pdf.info_box("Liens du projet", [
        ("Depot GitHub", "https://github.com/John271200/TP1Recommendation-system.git"),
        ("Application", "https://tp1recommendation-system.streamlit.app/"),
        ("Acces prof.", "johnaoga@gmail.com"),
    ])

    pdf.heading("Introduction", "1")
    pdf.paragraph(
        "Les systemes de recommandation sont presents dans de nombreux services numeriques : plateformes de streaming, commerce electronique, "
        "reseaux sociaux et bibliotheques numeriques. Leur role est d'aider l'utilisateur a trouver rapidement des contenus pertinents."
    )
    pdf.paragraph(
        "Dans ce TP, l'approche utilisee est le filtrage collaboratif item-item. Elle compare les items entre eux a partir des notes donnees "
        "par les utilisateurs. Deux films sont proches si les utilisateurs les evaluent de maniere similaire."
    )

    pdf.heading("Objectifs du projet", "2")
    pdf.bullet([
        "Lire et exploiter un dataset utilisateur-item.",
        "Construire les structures de donnees necessaires au filtrage collaboratif.",
        "Calculer la similarite cosinus entre les items.",
        "Predire les scores des items non notes par un utilisateur.",
        "Afficher une liste top-N de recommandations.",
        "Proposer une interface web interactive avec Streamlit.",
        "Publier le projet sur GitHub et le deployer en ligne.",
    ])

    pdf.heading("Donnees utilisees", "3")
    pdf.paragraph(
        "Le projet utilise deux fichiers CSV. Le fichier ratings.csv contient les notes donnees par les utilisateurs. "
        "Le fichier items.csv associe les identifiants des items aux titres des films."
    )
    pdf.table(
        ["Fichier", "Role", "Colonnes"],
        [
            ["ratings.csv", "Notes utilisateur-item", "user_id, item_id, rating"],
            ["items.csv", "Description des films", "item_id, title"],
        ],
        [105, 185, 197],
    )
    pdf.paragraph("Le dataset contient 8 utilisateurs, 8 films et 32 notes. Il est volontairement reduit pour faciliter l'analyse du fonctionnement de l'algorithme.")

    pdf.heading("Architecture du projet", "4")
    pdf.code_block([
        "TP1/",
        "  app.py",
        "  recommender.py",
        "  ratings.csv",
        "  items.csv",
        "  requirements.txt",
        "  README.md",
        "  EXECUTION_SUMMARY.md",
        "  SUBMISSION_LINKS.md",
        "  RAPPORT_TP1_AGBESSI_John_Ulrich.pdf",
    ])
    pdf.table(
        ["Fichier", "Description"],
        [
            ["recommender.py", "Logique de recommandation item-item"],
            ["app.py", "Interface web Streamlit"],
            ["ratings.csv", "Notes des utilisateurs"],
            ["items.csv", "Titres des films"],
            ["requirements.txt", "Dependance Streamlit"],
        ],
        [135, 352],
    )

    pdf.heading("Methode de recommandation", "5")
    pdf.subheading("5.1 Filtrage collaboratif item-item")
    pdf.paragraph(
        "Le filtrage collaboratif item-item cherche les items similaires aux items deja apprecies par l'utilisateur. "
        "Cette approche est interpretable : un film est recommande parce qu'il est proche d'autres films deja notes."
    )
    pdf.subheading("5.2 Structures de donnees")
    pdf.bullet([
        "ratings_by_user : dictionnaire permettant de retrouver les notes d'un utilisateur.",
        "ratings_by_item : dictionnaire permettant de retrouver les notes recues par un item.",
    ])
    pdf.subheading("5.3 Similarite cosinus")
    pdf.paragraph("Chaque item est represente par un vecteur de notes. Les notes manquantes sont remplacees par 0.")
    pdf.code_block(["similarite(A, B) = (A . B) / (||A|| * ||B||)"])
    pdf.subheading("5.4 Prediction des scores")
    pdf.paragraph("Pour chaque item candidat, le score predit est calcule avec une moyenne ponderee par les similarites.")
    pdf.code_block(["score(item) = somme(similarite(item, item_note) * note) / somme(abs(similarite))"])

    pdf.heading("Interface Streamlit", "6")
    pdf.paragraph(
        "L'interface Streamlit rend le systeme accessible depuis un navigateur. Elle permet de choisir l'utilisateur cible, de regler le nombre "
        "de recommandations, de consulter les notes deja donnees et de visualiser les similarites item-item."
    )
    pdf.bullet([
        "Selection de l'utilisateur cible.",
        "Choix du nombre de recommandations top-N.",
        "Affichage des notes de l'utilisateur.",
        "Affichage des recommandations.",
        "Affichage des meilleures similarites item-item.",
    ])

    pdf.heading("Execution du projet", "7")
    pdf.subheading("7.1 Installation")
    pdf.code_block(["python -m pip install -r requirements.txt"])
    pdf.subheading("7.2 Lancement Streamlit")
    pdf.code_block(["streamlit run app.py"])
    pdf.subheading("7.3 Execution console")
    pdf.code_block(["python recommender.py --user U1 --top-n 3 --show-similarities"])

    pdf.heading("Resultats obtenus", "8")
    pdf.code_block([
        "Top similarites item-item",
        "John Wick <-> Mad Max Fury Road : 0.986",
        "The Matrix <-> Mad Max Fury Road : 0.977",
        "The Matrix <-> John Wick : 0.962",
        "Inception <-> The Martian : 0.898",
        "Interstellar <-> The Martian : 0.828",
        "",
        "Recommandations top-3 pour U1",
        "1. Gravity (I7) - score predit : 4.27",
        "2. Blade Runner 2049 (I8) - score predit : 2.69",
        "3. John Wick (I4) - score predit : 1.94",
    ])
    pdf.paragraph(
        "Pour l'utilisateur U1, les films deja notes sont exclus des recommandations. Gravity obtient le meilleur score predit, "
        "ce qui indique que ce film est le plus pertinent selon les similarites calculees avec les films deja notes par l'utilisateur."
    )

    pdf.heading("Deploiement", "9")
    pdf.paragraph("Le depot GitHub et l'application Streamlit sont disponibles en ligne.")
    pdf.info_box("Informations de soumission", [
        ("GitHub", "https://github.com/John271200/TP1Recommendation-system.git"),
        ("Streamlit", "https://tp1recommendation-system.streamlit.app/"),
        ("Professeur", "johnaoga@gmail.com"),
    ])

    pdf.heading("Limites et perspectives", "10")
    pdf.subheading("10.1 Limites")
    pdf.bullet([
        "Le dataset est petit et sert principalement a illustrer l'algorithme.",
        "Les notes manquantes sont remplacees par 0 pour simplifier le calcul.",
        "Le probleme de cold start n'est pas encore traite.",
        "Le modele n'est pas encore evalue avec des metriques comme RMSE, precision ou recall.",
    ])
    pdf.subheading("10.2 Ameliorations possibles")
    pdf.bullet([
        "Utiliser un dataset plus grand comme MovieLens.",
        "Ajouter une separation train/test.",
        "Comparer les approches item-item et user-user.",
        "Ajouter l'import de fichiers CSV depuis Streamlit.",
        "Ameliorer l'interface avec des graphiques et une matrice de similarite.",
    ])

    pdf.heading("Conclusion", "11")
    pdf.paragraph(
        "Ce TP a permis de realiser un systeme de recommandation top-N complet, depuis la lecture des donnees jusqu'au deploiement d'une interface web. "
        "Le filtrage collaboratif item-item offre une approche claire et interpretable pour comprendre les bases des systemes de recommandation."
    )
    pdf.paragraph(
        "L'application Streamlit complete le projet en rendant les recommandations facilement testables. Le depot GitHub et le lien de deploiement "
        "permettent au professeur de consulter le code et d'executer l'application en ligne."
    )

    pdf.finish()
    return pdf.pages


def write_pdf(pages):
    objects = []

    def add_object(content):
        objects.append(content)
        return len(objects)

    catalog_id = add_object("<< /Type /Catalog /Pages 2 0 R >>")
    pages_id = add_object("")
    font_regular_id = add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    font_bold_id = add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
    font_mono_id = add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>")

    page_ids = []
    total_pages = len(pages)
    for index, commands in enumerate(pages, start=1):
        page_commands = list(commands)
        if index > 1:
            page_commands.insert(0, f"{BLUE} rg")
            page_commands.insert(1, f"0 {PAGE_HEIGHT - 38} {PAGE_WIDTH} 38 re f")
            page_commands.extend([
                "BT",
                f"{WHITE} rg",
                "/F2 10 Tf",
                f"{LEFT} {PAGE_HEIGHT - 24} Td (TP1 - Recommendation system item-item) Tj",
                "ET",
                f"{GRAY} RG",
                f"0.6 w",
                f"{LEFT} 42 m {PAGE_WIDTH - RIGHT} 42 l S",
                "BT",
                f"{GRAY} rg",
                "/F1 9 Tf",
                f"{LEFT} 25 Td (AGBESSI John Ulrich - Genie logiciel - IFRI-UAC) Tj",
                "ET",
                "BT",
                f"{GRAY} rg",
                "/F1 9 Tf",
                f"{PAGE_WIDTH - RIGHT - 55} 25 Td (Page {index}/{total_pages}) Tj",
                "ET",
            ])
        stream = "\n".join(page_commands)
        stream_bytes = stream.encode("latin-1", errors="replace")
        content_id = add_object(f"<< /Length {len(stream_bytes)} >>\nstream\n{stream}\nendstream")
        page_id = add_object(
            f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
            f"/Resources << /Font << /F1 {font_regular_id} 0 R /F2 {font_bold_id} 0 R /F3 {font_mono_id} 0 R >> >> "
            f"/Contents {content_id} 0 R >>"
        )
        page_ids.append(page_id)

    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    objects[pages_id - 1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>"

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for obj_id, content in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{obj_id} 0 obj\n".encode("latin-1"))
        pdf.extend(content.encode("latin-1", errors="replace"))
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))
    pdf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n".encode("latin-1")
    )
    OUTPUT_PATH.write_bytes(pdf)


if __name__ == "__main__":
    write_pdf(build_report())
    print(OUTPUT_PATH)
