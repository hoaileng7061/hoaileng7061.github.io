# Shiyi Wei’s academic website

This is the complete handoff folder for Shiyi. It contains the website source, profile photo, publication records, and the finished English and French CV PDFs. It is ready to preview locally and publish to **Shiyi’s own GitHub account**.

No files outside this folder are required. There is no Git history, remote, login or hosting account attached. The original reference documents are intentionally excluded; they are not needed to build or publish the site.

## 1. Start here with your local Codex

Extract the ZIP if necessary, then open **this folder** as the project in your local Codex. The correct folder contains `build.py`, this README, and the hidden `.github` folder.

Paste the following prompt, filling in your actual GitHub username:

```text
This is my completed academic website. My GitHub username is: YOUR_ACTUAL_USERNAME.

Read README.md, AGENTS.md and CODEX_HANDOFF.md. Preview and check the supplied
website, then publish it to my own GitHub account as my personal GitHub Pages
site at https://MY-USERNAME.github.io/.

Use the repository named MY-USERNAME.github.io, using my actual lowercase
username in the repository name. Verify the authenticated account belongs
to me before creating a repository or pushing. If authentication is needed,
guide me through signing in on my computer.

Keep the existing design and content, including both supplied CV PDFs.
Do not rebuild the PDFs just to publish the website. Preserve any existing
repository or site you find rather than overwriting it automatically.

Complete the GitHub Pages setup, explicitly trigger the supplied workflow,
wait for a successful deployment, and verify the actual public URL, photo,
all three pages, both CV downloads and the publication links. Do not stop
after merely pushing the source files. Report the final URL and any real
remaining blocker.
```

`CODEX_HANDOFF.md` provides the precise publishing sequence and acceptance checks. Authentication and publishing happen on Shiyi’s computer using her account.

## 2. Does the website need a name?

- **Displayed title:** already set to **Shiyi Wei**. No separate brand name is needed.
- **GitHub account:** use Shiyi’s existing account, or choose a username when creating one.
- **Recommended repository:** `username.github.io`, replacing `username` with the actual lowercase GitHub username.
- **Resulting address:** `https://username.github.io/`.

For example, if the username were `shiyi-example`, the repository would be `shiyi-example.github.io`, and the address would be `https://shiyi-example.github.io/`. This is an illustration, not an account or domain that has been reserved.

A different repository name is also supported. A repository named `academic-website` would normally appear at `https://username.github.io/academic-website/`; the workflow handles that URL prefix automatically. A custom domain is optional and not required for the initial publication. Renaming this local folder does not change the website’s title or future address.

## 3. Preview locally

**Required:** Python 3.10 or newer. The website uses only Python’s standard library. There is no package-installation, Node, Ruby, Jekyll, Docker or LaTeX step for building and publishing the supplied site.

From a terminal opened in this folder:

```sh
python3 preview.py
```

Open <http://127.0.0.1:4002/>. The preview rebuilds when source files change; refresh the browser after saving. Stop it with Control-C.

On Windows, use `py -3 preview.py` if `python3` is not available. If port 4002 is occupied, run `python3 preview.py --port 4003` and open the address it prints.

Localhost addresses are local previews, not public URLs. Do not put them in GitHub Pages settings. Use the preview server instead of double-clicking generated HTML files.

To build without starting a server:

```sh
python3 build.py
```

The output is written to `dist/`. A build removes obsolete generated files. `dist/` is ignored by Git; the GitHub workflow rebuilds it from the source.

## 4. Publish with GitHub Pages

The full instructions for Codex are in `CODEX_HANDOFF.md`. The sequence is:

1. Verify the logged-in GitHub identity is Shiyi’s account and establish the repository name.
2. Create a new repository, or inspect an existing one before changing it. A GitHub Free personal Pages site uses a **public** repository.
3. Put this folder’s **contents at the repository root**, on branch `main`. Include `.github/workflows/pages.yml` and `.gitignore`. Do not put the whole project inside another wrapper directory in the repository.
4. Commit and push the source, including the two finished PDFs in `files/`.
5. In **Settings → Pages → Build and deployment**, choose **GitHub Actions** as the source. This initial setting is required; the supplied workflow does not enable Pages by itself.
6. Explicitly run `.github/workflows/pages.yml` after enabling Pages. An early run from the first push may fail if Pages was not enabled yet; run it again after setup.
7. Wait for the workflow to succeed and verify the public address returned by GitHub Pages.

Use GitHub Actions, not a branch-based Jekyll build. Python runs during the build; visitors receive static HTML, CSS, images and PDFs. There is no Python server to host.

The workflow computes the URL prefix for either a personal site or project site. To simulate a project-site prefix locally:

```sh
python3 build.py --base-path /academic-website
```

The regular preview uses an empty prefix. No hostname is hard-coded into the site. No custom domain or verification token has been carried over from another website.

## 5. What is in this folder?

| Path | Purpose |
| --- | --- |
| `data/profile.json` | English biography, education, research experience, languages and contact information |
| `data/profile.fr.json` | French CV wording; keep its facts consistent with the English version |
| `data/publications.json` | Shared titles, authors, journal information, DOI and arXiv identifiers |
| `assets/shiyi.jpg` | Supplied profile photo |
| `assets/site.css` | Layout, typography, colors and mobile styling |
| `templates/base.html` | Shared navigation, sidebar and footer |
| `files/shiyi-wei-cv.pdf` | Finished English CV, included in the deployment |
| `files/shiyi-wei-cv-fr.pdf` | Finished French CV, included in the deployment |
| `build.py` / `preview.py` | Static build and local preview |
| `cv/` | CV builder, academic style file, instructions and generated LaTeX examples |
| `.github/workflows/pages.yml` | GitHub Pages build and deployment workflow |
| `SOURCES.md` | Content provenance and factual interpretation notes |

The site has **About**, **Publications** and **CV** pages. There is no Teaching page. The CVs omit private tutoring and physics/technical skills lists, retaining Languages. Expected PhD completion is October 2027.

## 6. Maintain the site

Edit the JSON files or ask Codex to make a change, then build or refresh the preview. Preserve publication author order. Each paper’s `published` date determines ordering; paper links and BibTeX exports are generated from its metadata.

Publication entries intentionally contain titles, author lists, journal citations and links only. Do not add generated summaries or abstracts unless Shiyi requests them.

**Website builds do not regenerate the PDF CVs.** If changing facts that also belong in the CVs, update both language records and regenerate both PDFs before the next deployment:

```sh
python3 cv/build_cv.py --language en
python3 cv/build_cv.py --language fr
python3 build.py
```

Only this optional PDF regeneration needs `latexmk`, XeLaTeX and Times New Roman. See `cv/README.md`. The finished PDFs are supplied, so a machine without LaTeX can still preview, publish and make website-only changes. Do not silently substitute a different CV font to work around a missing local font.

After regenerating the PDFs, inspect both languages and check their downloads. Commit the PDFs under `files/`; temporary PDFs and LaTeX logs under `cv/` are ignored.

For later website updates, push changes to `main`; the workflow redeploys automatically once Pages is configured.

## 7. Final publishing checks

- The public URL belongs to Shiyi’s selected account and repository.
- About, Publications and CV pages load, with correct active navigation.
- The portrait and stylesheet load on desktop and mobile.
- Both publication records, journal/arXiv links and bibliography downloads work.
- English and French CV buttons download the correct PDFs.
- Dates, supervisors and author lists remain accurate, and excluded sections stay excluded.
- Public navigation, assets and CV links use the published site, without localhost URLs.

## References

- [GitHub Pages naming and creation](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [Custom GitHub Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- Design reference: <https://htcmath.github.io/> and AcademicPages. This site’s templates and stylesheet were written for Shiyi; the CV uses the supplied academic style.
