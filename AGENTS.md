# Project instructions

Read `README.md` and `CODEX_HANDOFF.md` before publishing or changing this site.

- Work only in this website folder; preserve unrelated files and existing work.
- Keep the Python 3.10+ standard-library build. Do not migrate to Node, Jekyll or Docker.
- Build with `python3 build.py`; preview with `python3 preview.py` on port 4002.
- Treat `data/profile.json`, `data/profile.fr.json` and `data/publications.json` as the content sources.
- Keep English and French dates, institutions, supervisors and research facts consistent.
- The PhD began in November 2024; completion is expected in October 2027.
- Keep the doctoral research role ongoing; expected completion is not a completed degree.
- Preserve ENS diploma and ICFP details. Sorbonne Licence 1 and 2 are not a completed bachelor's degree.
- Distinguish the initial thesis project and proposed research from completed results.
- Preserve exact published paper titles, author order, journal status, DOI and arXiv identifiers.
- Publication entries contain bibliographic details and links only. Do not add generated summaries or abstracts unless Shiyi asks for them.
- Do not add private tutoring, Teaching pages or sections, or skills lists; retain Languages.
- Do not restore application-specific text or copy private reference PDFs into the site.
- Keep the supplied portrait and academic layout unless Shiyi requests a change.
- Publish the included English and French PDFs without requiring LaTeX on the deployment runner.
- For CV edits, follow `cv/README.md`, rebuild both languages and inspect every PDF page.
- Regenerate `dist/` after changing content or PDFs; do not edit generated HTML directly.
- Check links, downloads, publication metadata, and desktop/mobile layouts after changes.
- Keep `.github/workflows/pages.yml` and `.gitignore`; exclude caches and LaTeX auxiliary files.
- Publish only when Shiyi asks. Then continue through deployment and live verification.
- Verify Shiyi's actual GitHub login and chosen Git author identity before repository changes.
- Preserve existing repositories/sites; resolve collisions before replacing any content.
- Never include credentials, another person's Git history, or machine-specific paths.
- Follow the Pages bootstrap and explicit workflow dispatch in `CODEX_HANDOFF.md`.
