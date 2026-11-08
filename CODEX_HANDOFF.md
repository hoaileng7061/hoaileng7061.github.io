# Publishing this website from Shiyi's computer

This is a complete local website for Shiyi Wei. Use these instructions when Shiyi
asks her local Codex to publish it using **her GitHub account**. The handoff itself
does not publish anything.

Read `README.md` and `AGENTS.md` first. Once Shiyi has asked for publication,
continue through setup, deployment and live verification. Ask only when necessary
account access, identity information or an existing-site conflict is unresolved.

## 1. Open the correct folder

Work inside the extracted folder containing `build.py`, `README.md`, `data/`, and
`.github/`. Its **contents must become the repository root**. Do not put the whole
folder inside another directory in the repository.

The package should include:

- `.github/workflows/pages.yml` and `.gitignore`, including their leading dots.
- `build.py`, `preview.py`, `templates/`, `assets/`, and `data/`.
- `files/shiyi-wei-cv.pdf` and `files/shiyi-wei-cv-fr.pdf`.
- `cv/` with its builder, style, generated TeX sources and instructions.
- `README.md`, `CODEX_HANDOFF.md`, `AGENTS.md`, and `SOURCES.md`.

Private reference documents are intentionally excluded and are not needed to
build or publish the site. Do not add credentials, another person's Git history,
screenshots, Python caches, LaTeX auxiliary files or the generated `dist/` folder.
Do not rely on a file-picker selection that silently omits `.github/`.

## 2. Check the site locally

The website needs **Python 3.10 or newer** and its standard library. No Node,
Jekyll, Docker or package installation is needed for the website build. Keep the
existing implementation.

```sh
python3 --version
python3 build.py
python3 preview.py
```

Open `http://127.0.0.1:4002/` and inspect About, Publications and CV. Stop the local
preview with Control-C when finished. If Python is installed under the command
`python` instead, use that executable after checking its version.

**Do not rebuild the PDFs merely to publish the site.** Both finished PDFs are
included. GitHub Actions copies them into the website without running LaTeX.
Future PDF edits require XeLaTeX, `latexmk`, Times New Roman and the packages used
by `cv/simplecv.sty`. Follow `cv/README.md` when rebuilding. Keep the English and
French profile records consistent; published paper metadata is shared.

## 3. Verify Shiyi's account and choose the URL

Git and GitHub CLI (`gh`) are needed for the command-line publishing steps.
Inspect authentication before creating a repository or pushing:

```sh
gh auth status --hostname github.com
gh api user --jq .login
```

The returned login must be Shiyi's intended account. If authentication is absent
or points to another account, have Shiyi complete the normal GitHub sign-in or
account switch. Never ask her to paste a password or token into these files.

The visible website name is already **Shiyi Wei**. For a personal GitHub Pages
site, use a public repository named **the actual lowercase GitHub username plus
`.github.io`**. Its address will be `https://username.github.io/`. Do not invent a
username or assume that a name such as `shiyi-wei` is her account.

A project repository is also supported, with an address such as
`https://username.github.io/academic-website/`. The included workflow obtains the
correct path prefix from GitHub Pages automatically. Choose this alternative with
Shiyi if her existing personal site should be preserved.

In the commands below, replace **OWNER** with her verified GitHub login and
**REPO** with the chosen repository name. These are placeholders, not literal
values to execute.

## 4. Preserve existing work, then push the source

Check whether the destination already exists:

```sh
gh repo view OWNER/REPO --json nameWithOwner,url,defaultBranchRef
```

Distinguish a missing repository from an authentication or permission error. If
the repository contains an existing website or other work, inspect it and resolve
the intended destination before changing it. Preserve unrelated content; do not
force-push, reset history or replace an existing site without authorization.

If this extracted folder already contains `.git`, inspect its status, history and
remotes first. Otherwise, initialize a fresh repository:

```sh
git init -b main
git config user.name
git config user.email
```

Use Shiyi's own chosen Git author name and email. If these are missing or belong
to someone else, obtain her preferred identity and set it for this repository.
Do not copy the original preparer's Git configuration or history.

For a new destination repository, stage the source and inspect the complete list
before committing:

```sh
git add .
git diff --cached --name-only
git diff --cached --stat
git commit -m "Add Shiyi Wei academic website"
gh repo create OWNER/REPO --public --source=. --remote=origin --push
```

Confirm that the staged files include `.github/workflows/pages.yml` and both
PDFs, and exclude generated output and private material. The workflow listens for
pushes to `main`, so retain that branch name. A public repository supports this
deployment on GitHub Free.

## 5. Enable GitHub Pages, then dispatch the workflow

After the source has been pushed, configure the repository's Pages source as
**GitHub Actions**. In the browser, use **Settings → Pages → Build and deployment
→ Source → GitHub Actions**.

Alternatively, inspect the Pages setting using the authenticated CLI:

```sh
gh api repos/OWNER/REPO/pages
```

If the repository is accessible but has no Pages configuration, create it:

```sh
gh api --method POST repos/OWNER/REPO/pages -f build_type=workflow
```

If Pages is already configured for another build type, update the setting only
after resolving any existing-site conflict:

```sh
gh api --method PUT repos/OWNER/REPO/pages -f build_type=workflow
```

Do not change a setting that is already correct. Creating or updating Pages
requires the appropriate repository administration and Pages permissions.

The initial push may start a workflow before Pages has been enabled. If that run
fails at configuration, enable Pages and start a fresh run. The included
`configure-pages` action does not enable Pages by default; do not add a personal
access token to the repository to bypass this setup.

Explicitly start and watch a run after Pages is configured:

```sh
gh workflow run pages.yml --repo OWNER/REPO --ref main
gh run list --repo OWNER/REPO --workflow pages.yml --limit 5
gh run watch RUN_ID --repo OWNER/REPO --exit-status
```

Replace **RUN_ID** with the newly dispatched run's ID. If it fails, inspect the
failure before changing anything:

```sh
gh run view RUN_ID --repo OWNER/REPO --log-failed
```

The workflow builds with Python, uploads `dist/` and deploys it to GitHub Pages.
It needs neither a separate hosting service nor a branch containing built HTML.

Official references:

- [GitHub Pages REST API: creation and updates](https://docs.github.com/en/rest/pages/pages#create-a-github-pages-site).
- [Configure Pages action and its enablement option](https://github.com/actions/configure-pages/blob/v5/action.yml).
- [Custom GitHub Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## 6. Verify the live result

Retrieve the actual Pages URL instead of guessing it:

```sh
gh api repos/OWNER/REPO/pages --jq .html_url
```

After the deployment succeeds, open that URL and verify:

- About, Publications and CV all load, with correct navigation and the portrait.
- Both published papers appear with their exact titles, author order, journal
  references, DOI and arXiv links.
- Publication entries contain bibliographic details and links only, without added
  summaries or abstracts unless Shiyi requests them.
- Both English and French CV downloads open and show the expected October 2027
  PhD completion date, clearly marked as expected.
- Individual BibTeX links and the complete bibliography download work.
- Desktop and mobile layouts remain readable, without horizontal overflow.
- There is no Teaching page, private-tutoring content or skills section. Languages
  remain included.

Report the live site URL, repository URL and successful deployment result. If a
required account action remains blocked, state that exact action. A successful
push alone is not a verified deployment.
