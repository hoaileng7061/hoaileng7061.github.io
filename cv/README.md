# Academic CV

The CV uses the supplied academic CV's original `simplecv.sty`, US Letter paper,
10-point Times New Roman, and MidnightBlue headings. The PDF contains Shiyi's
research interests, education, publications, research experience, and languages.

## Update and build

Edit the website's shared English records in `data/profile.json`, the French
profile in `data/profile.fr.json`, and publications in `data/publications.json`.
Then run from the site directory:

```sh
python3 cv/build_cv.py
python3 cv/build_cv.py --language fr
```

The default language is English (`--language en`). The builder generates
`cv/shiyi-wei-cv.tex` and writes the English PDF to `files/shiyi-wei-cv.pdf`.
French outputs use the suffix `-fr`: `cv/shiyi-wei-cv-fr.tex` and
`files/shiyi-wei-cv-fr.pdf`. Published paper titles and author names remain in
their original form in both versions. Do not edit the generated TeX files
directly. Rebuild the website after rebuilding the PDFs so the downloads in
`dist/` are refreshed.

Requirements: Python 3, `latexmk`, XeLaTeX, and the Times New Roman font. No Python
packages are required. The build stops on TeX errors, overflowing boxes, or missing
characters. The original style may report that Times New Roman has no small-caps
variant; it uses the regular face for section headings, matching the reference.

Education records contain `university`, `location`, `degree`, `dates`, an
`advisors` list, and optional `details`. An optional `advisor_roles` list supplies
one role per advisor, such as thesis director or co-supervisor. Empty dates remain
blank; use `In progress` only when that status is confirmed. Add only confirmed
education and dates. Publication author order comes directly from the JSON, with
Shiyi's name in bold.

Research experience records contain `role`, `institution`, `location`, `dates`,
`advisors`, and `description`. Languages are records with `language` and `level`.
The CV deliberately excludes private tutoring and skills lists. Historical thesis
plans should remain labelled as an initial project, rather than completed results.

## Visual check

After changing content, render and inspect every page:

```sh
mkdir -p /tmp/shiyi-cv-preview
pdftoppm -png -r 140 files/shiyi-wei-cv.pdf /tmp/shiyi-cv-preview/page
pdftoppm -png -r 140 files/shiyi-wei-cv-fr.pdf /tmp/shiyi-cv-preview/page-fr
```

Check for clipping, unwanted page breaks, and incorrect characters. The layout
can grow naturally when more verified education or other content is added.
