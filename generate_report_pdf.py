from pathlib import Path
import textwrap


BASE_DIR = Path(__file__).parent
OUTPUT_PATH = BASE_DIR / "RAPPORT_TP1_AGBESSI_John_Ulrich.pdf"


REPORT_LINES = [
    ("title", "Rapport TP1"),
    ("subtitle", "Recommendation system: Collaborative Filtering item-item top-N"),
    ("normal", ""),
    ("normal", "Nom et prenoms : AGBESSI John Ulrich"),
    ("normal", "Filiere : Genie logiciel"),
    ("normal", "Ecole : IFRI-UAC"),
    ("normal", "Depot GitHub : https://github.com/John271200/TP1Recommendation-system.git"),
    ("normal", "Application Streamlit : https://tp1recommendation-system.streamlit.app/"),
    ("normal", ""),
    ("heading", "1. Introduction"),
    ("normal", "Ce projet porte sur la realisation d'un systeme de recommandation base sur le filtrage collaboratif item-item. L'objectif est de proposer a un utilisateur une liste top-N d'items qu'il n'a pas encore notes, en utilisant les notes donnees par l'ensemble des utilisateurs."),
    ("normal", "Le projet contient aussi une interface Streamlit permettant de tester facilement le systeme depuis un navigateur."),
    ("heading", "2. Objectif du projet"),
    ("normal", "L'objectif principal est de construire une application capable de lire un fichier de notes utilisateur-item, calculer les similarites entre les items, predire les scores des items non notes par un utilisateur et afficher les meilleures recommandations top-N."),
    ("heading", "3. Donnees utilisees"),
    ("normal", "Le projet utilise deux fichiers CSV. Le fichier ratings.csv contient les notes donnees par les utilisateurs. Le fichier items.csv contient les noms des items. Dans ce TP, les items representent des films."),
    ("code", "user_id,item_id,rating"),
    ("code", "U1,I1,5"),
    ("code", "U1,I2,4"),
    ("code", "item_id,title"),
    ("code", "I1,Inception"),
    ("code", "I2,Interstellar"),
    ("heading", "4. Methode utilisee"),
    ("normal", "La methode utilisee est le filtrage collaboratif item-item. Elle consiste a comparer les items entre eux a partir des notes donnees par les utilisateurs."),
    ("normal", "Le programme construit une structure utilisateur-item pour connaitre les notes de chaque utilisateur, puis une structure item-utilisateur pour connaitre les utilisateurs ayant note chaque item."),
    ("normal", "Pour chaque paire d'items, le programme construit deux vecteurs de notes. Une note manquante est consideree comme 0. La similarite utilisee est la similarite cosinus."),
    ("code", "similarite(A, B) = produit_scalaire(A, B) / (norme(A) * norme(B))"),
    ("normal", "Pour un utilisateur cible, le programme ignore les items deja notes. Pour chaque item candidat, il calcule un score predit avec une moyenne ponderee par les similarites."),
    ("code", "score(item) = somme(similarite * note) / somme(abs(similarite))"),
    ("heading", "5. Implementation"),
    ("normal", "Le fichier recommender.py contient l'implementation de l'algorithme de recommandation. Le fichier app.py contient l'interface Streamlit. Les fichiers ratings.csv et items.csv contiennent les donnees. Le fichier requirements.txt contient la dependance Streamlit."),
    ("normal", "L'application Streamlit permet de choisir un utilisateur, choisir le nombre de recommandations, afficher les notes deja donnees et afficher les similarites item-item."),
    ("heading", "6. Resultats obtenus"),
    ("normal", "La commande console suivante a ete testee :"),
    ("code", "python recommender.py --user U1 --top-n 3 --show-similarities"),
    ("normal", "Resultat obtenu :"),
    ("code", "Top similarites item-item"),
    ("code", "John Wick <-> Mad Max Fury Road : 0.986"),
    ("code", "The Matrix <-> Mad Max Fury Road : 0.977"),
    ("code", "The Matrix <-> John Wick : 0.962"),
    ("code", "Inception <-> The Martian : 0.898"),
    ("code", "Interstellar <-> The Martian : 0.828"),
    ("code", "Recommandations top-3 pour U1"),
    ("code", "1. Gravity (I7) - score predit : 4.27"),
    ("code", "2. Blade Runner 2049 (I8) - score predit : 2.69"),
    ("code", "3. John Wick (I4) - score predit : 1.94"),
    ("normal", "Pour l'utilisateur U1, les films deja notes sont exclus des recommandations. Le systeme propose donc seulement des items non notes par cet utilisateur."),
    ("heading", "7. Deploiement"),
    ("normal", "Le projet est disponible sur GitHub : https://github.com/John271200/TP1Recommendation-system.git"),
    ("normal", "L'application Streamlit est disponible ici : https://tp1recommendation-system.streamlit.app/"),
    ("normal", "Le professeur peut acceder au depot avec l'adresse : johnaoga@gmail.com"),
    ("heading", "8. Conclusion"),
    ("normal", "Ce TP a permis de mettre en place un systeme de recommandation top-N avec filtrage collaboratif item-item. L'approche est simple, interpretable et efficace pour comprendre les bases des systemes de recommandation."),
    ("normal", "L'ajout de Streamlit rend le projet plus accessible, car l'utilisateur peut tester les recommandations directement dans une interface web."),
]


def pdf_escape(text):
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_pages():
    pages = []
    current = []
    y = 790

    for style, text in REPORT_LINES:
        font_size = {"title": 22, "subtitle": 14, "heading": 14, "normal": 11, "code": 10}[style]
        leading = font_size + 6
        width = 52 if style in {"normal", "subtitle"} else 80
        if style == "title":
            width = 60
        wrapped = textwrap.wrap(text, width=width) if text else [""]

        for line in wrapped:
            if y < 55:
                pages.append(current)
                current = []
                y = 790
            current.append((style, font_size, 55, y, line))
            y -= leading

        if style in {"title", "subtitle", "heading"}:
            y -= 4

    if current:
        pages.append(current)
    return pages


def make_pdf():
    pages = build_pages()
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
    for page in pages:
        commands = ["BT"]
        for style, size, x, y, text in page:
            font = "/F2" if style in {"title", "heading"} else "/F3" if style == "code" else "/F1"
            commands.append(f"{font} {size} Tf")
            commands.append(f"{x} {y} Td ({pdf_escape(text)}) Tj")
            commands.append(f"{-x} {-y} Td")
        commands.append("ET")
        stream = "\n".join(commands)
        stream_bytes = stream.encode("latin-1", errors="replace")
        content_id = add_object(f"<< /Length {len(stream_bytes)} >>\nstream\n{stream}\nendstream")
        page_id = add_object(
            f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 595 842] "
            f"/Resources << /Font << /F1 {font_regular_id} 0 R /F2 {font_bold_id} 0 R /F3 {font_mono_id} 0 R >> >> "
            f"/Contents {content_id} 0 R >>"
        )
        page_ids.append(page_id)

    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    objects[pages_id - 1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>"

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, content in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{index} 0 obj\n".encode("latin-1"))
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
    make_pdf()
    print(OUTPUT_PATH)
