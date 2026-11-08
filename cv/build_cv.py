#!/usr/bin/env python3
"""Build the academic CV from the website's shared JSON records."""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


CV_DIR = Path(__file__).resolve().parent
SITE_DIR = CV_DIR.parent
LABELS = {
    "en": {
        "research": "Research Interests",
        "research_lead": "My research interests are in ",
        "education": "Education",
        "publications": "Publications",
        "experience": "Research Experience",
        "languages": "Languages",
        "email": "Email",
        "advisor": "Advisor",
        "advisors": "Advisors",
        "and": "and",
    },
    "fr": {
        "research": "Intérêts de recherche",
        "research_lead": "",
        "education": "Formation",
        "publications": "Publications",
        "experience": "Expérience en recherche",
        "languages": "Langues",
        "email": "Courriel",
        "advisor": "Encadrant",
        "advisors": "Encadrants",
        "and": "et",
    },
}


def latex_escape(value):
    """Render literal JSON text safely in a LaTeX argument."""
    escapes = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "$": r"\$",
        "&": r"\&",
        "#": r"\#",
        "%": r"\%",
        "_": r"\_",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "\n": " ",
        "\r": " ",
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "--",
        "\u2013": "--",
        "\u2014": "---",
    }
    return "".join(escapes.get(char, char) for char in str(value))


def join_names(names, conjunction="and"):
    if len(names) <= 1:
        return "".join(names)
    if len(names) == 2:
        return f" {conjunction} ".join(names)
    return ", ".join(names[:-1]) + f" {conjunction} " + names[-1]


def link(url, label):
    return r"\href{" + latex_escape(url) + "}{" + latex_escape(label) + "}"


def advisor_line(item, labels):
    advisors = item.get("advisors") or []
    roles = item.get("advisor_roles") or []
    if roles:
        if len(roles) != len(advisors):
            raise ValueError("advisor_roles must contain one role for each advisor.")
        return "; ".join(f"{role}: {name}" for role, name in zip(roles, advisors))
    if advisors:
        label = labels["advisor"] if len(advisors) == 1 else labels["advisors"]
        return label + ": " + join_names(advisors, labels["and"])
    return ""


def details_list(details):
    if not details:
        return ""
    entries = "\n".join(r"\entry{" + latex_escape(detail) + "}" for detail in details)
    return "\n" + r"\innerlist{" + "\n" + entries + "\n}"


def education_section(education, labels):
    if not education:
        return ""
    entries = []
    for item in education:
        university = latex_escape(item["university"])
        location = latex_escape(item.get("location", ""))
        degree = latex_escape(item["degree"])
        dates = latex_escape(item.get("dates") or "")
        advisor_text = latex_escape(advisor_line(item, labels))
        if advisor_text:
            entry = (
                r"\entrybigplus" + "\n"
                + r"{\textbf{" + university + "}}{" + location + "}\n"
                + "{" + degree + "}{" + dates + "}\n"
                + "{" + advisor_text + "}{}"
            )
        else:
            entry = (
                r"\entrybig" + "\n"
                + r"{\textbf{" + university + "}}{" + location + "}\n"
                + "{" + degree + "}{" + dates + "}"
            )
        entry += details_list(item.get("details") or [])
        entries.append(r"\begin{samepage}" + "\n" + entry + "\n" + r"\end{samepage}")
    return "\n".join([
        r"\section{" + latex_escape(labels["education"]) + "}",
        r"\outerlist{",
        "\n\n".join(entries),
        "}",
    ])


def publications_section(publications, name, labels):
    if not publications:
        return ""
    entries = []
    for paper in sorted(publications, key=lambda p: p.get("published", str(p["year"])), reverse=True):
        authors = [
            r"\textbf{" + latex_escape(author) + "}"
            if author == name else latex_escape(author)
            for author in paper["authors"]
        ]
        title = latex_escape(paper["title"])
        journal = latex_escape(paper["journal"])
        volume = latex_escape(paper["volume"])
        article = latex_escape(paper["article"])
        year = latex_escape(paper["year"])
        citation = (
            join_names(authors, labels["and"]) + '. "' + title + '." '
            + r"\textit{" + journal + r"} \textbf{" + volume + "}, "
            + article + " (" + year + ")."
        )
        references = []
        if paper.get("doi"):
            references.append(link("https://doi.org/" + paper["doi"], "doi:" + paper["doi"]))
        if paper.get("arxiv"):
            references.append(link("https://arxiv.org/abs/" + paper["arxiv"], "arXiv:" + paper["arxiv"]))
        if references:
            citation += " " + "; ".join(references) + "."
        entries.append(r"\entry{" + citation + "}")
    return "\n".join([
        r"\section{" + latex_escape(labels["publications"]) + "}",
        r"\orderedouterlist{",
        "\n".join(entries),
        "}",
    ])


def research_experience_section(experience, labels):
    if not experience:
        return ""
    entries = []
    for item in experience:
        institution = latex_escape(item["institution"])
        location = latex_escape(item.get("location", ""))
        role = latex_escape(item["role"])
        dates = latex_escape(item.get("dates", ""))
        entry = (
            r"\Needspace{8\baselineskip}" + "\n"
            + r"\begin{samepage}" + "\n"
            + r"\entrybig" + "\n"
            + r"{\parbox[t]{0.74\textwidth}{\raggedright\textbf{" + institution + "}}}{" + location + "}\n"
            + "{" + role + "}{" + dates + "}"
        )
        advisors = advisor_line(item, labels)
        if advisors:
            entry += "\n" + r"\par\vspace{2pt}{\small " + latex_escape(advisors) + r"\par}"
        if item.get("description"):
            entry += details_list([item["description"]])
        entry += "\n" + r"\end{samepage}"
        entries.append(entry)
    # Keep a short research section together when it would otherwise leave its
    # final entry alone on the next page. Long sections can still break by entry.
    reserve_lines = min(40, max(11, 7 * len(experience) + 3))
    return "\n".join([
        r"\Needspace{" + str(reserve_lines) + r"\baselineskip}",
        r"\section{" + latex_escape(labels["experience"]) + "}",
        r"\outerlist{",
        "\n\n".join(entries),
        "}",
    ])


def languages_section(languages, labels):
    if not languages:
        return ""
    entries = [
        r"\entry{\textbf{" + latex_escape(item["language"]) + ":} "
        + latex_escape(item["level"]) + "}"
        for item in languages
    ]
    return "\n".join([
        r"\Needspace{8\baselineskip}",
        r"\section{" + latex_escape(labels["languages"]) + "}",
        r"\outerlist{",
        "\n".join(entries),
        "}",
    ])


def make_document(profile, publications, language="en"):
    labels = LABELS[language]
    name = profile["name"]
    given_name, surname = name.rsplit(" ", 1)
    heading = profile.get("cv_name") or f"{surname.upper()} {given_name}"
    interests = profile.get("interests") or []
    sections = []
    if interests:
        phrases = [interest[:1].lower() + interest[1:] for interest in interests]
        if not labels["research_lead"]:
            phrases[0] = interests[0]
        sections.append(
            r"\section{" + latex_escape(labels["research"]) + "}\n\n"
            + latex_escape(labels["research_lead"] + join_names(phrases, labels["and"]) + ".")
        )
    education = education_section(profile.get("education") or [], labels)
    if education:
        sections.append(education)
    publications_tex = publications_section(publications, name, labels)
    if publications_tex:
        sections.append(publications_tex)
    research_experience = research_experience_section(profile.get("research_experience") or [], labels)
    if research_experience:
        sections.append(research_experience)
    languages = languages_section(profile.get("languages") or [], labels)
    if languages:
        sections.append(languages)
    preamble = r"""% Generated by cv/build_cv.py from the selected profile and publications JSON.
% Layout matches the supplied academic CV; edit the JSON records, not this file.
\documentclass[letterpaper,10pt]{article}
\def\theme{MidnightBlue}
\renewcommand{\baselinestretch}{1.0}
\selectfont
\usepackage{fontspec}
\setmainfont{Times New Roman}
\usepackage{simplecv}
\usepackage{needspace}

\begin{document}
"""
    if language == "fr":
        preamble = preamble.replace(
            r"\usepackage{simplecv}",
            r"\PassOptionsToPackage{french}{babel}" + "\n" + r"\usepackage{simplecv}",
        ).replace(r"\begin{document}", r"\begin{document}" + "\n" + r"\selectlanguage{french}")
    header = (
        r"\headinginline{" + latex_escape(heading) + "}{\n"
        + "    " + latex_escape(labels["email"]) + ": " + link("mailto:" + profile["email"], profile["email"]) + "\n"
        + "}\n\n"
    )
    return preamble + header + "\n\n".join(sections) + "\n\n" + r"\end{document}" + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=sorted(LABELS), default="en", help="CV language (default: en)")
    args = parser.parse_args()
    profile_name = "profile.fr.json" if args.language == "fr" else "profile.json"
    basename = "shiyi-wei-cv-fr" if args.language == "fr" else "shiyi-wei-cv"
    tex_path = CV_DIR / f"{basename}.tex"
    pdf_path = CV_DIR / f"{basename}.pdf"
    output_path = SITE_DIR / "files" / f"{basename}.pdf"
    profile = json.loads((SITE_DIR / "data" / profile_name).read_text(encoding="utf-8"))
    publications = json.loads((SITE_DIR / "data" / "publications.json").read_text(encoding="utf-8"))
    latexmk = shutil.which("latexmk")
    if latexmk is None:
        raise SystemExit("latexmk is required. Install a TeX distribution with XeLaTeX and Times New Roman.")
    tex_path.write_text(make_document(profile, publications, args.language), encoding="utf-8")
    result = subprocess.run(
        [latexmk, "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", tex_path.name],
        cwd=CV_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        sys.stderr.write(result.stdout + result.stderr)
        raise SystemExit(result.returncode)
    if not pdf_path.is_file() or not pdf_path.read_bytes().startswith(b"%PDF-"):
        raise SystemExit("XeLaTeX did not produce a valid PDF file.")
    log_path = CV_DIR / f"{basename}.log"
    log = log_path.read_text(encoding="utf-8", errors="replace")
    if re.search(r"Overfull \\[hv]box|Missing character:", log):
        raise SystemExit(f"The CV has overflowing text or missing glyphs; review {log_path} before publishing it.")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(pdf_path, output_path)
    print(f"Built {output_path}")
    page_match = re.search(r"Output written on .*?\((\d+) pages?", log)
    if page_match:
        print(f"Pages: {page_match.group(1)}")


if __name__ == "__main__":
    main()
