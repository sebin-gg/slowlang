# Account signups needed to ship the packages (manual steps)

Everything below needs your login/SSO - can't be automated. Ordered by payoff.

## 1. PyPI (claim `slowlang` AND `tortoiselang`)

PyPI has NO SSO - username + email + mandatory 2FA (TOTP).

1. Sign up at https://pypi.org/account/register/ (verify email).
2. Enable 2FA in account settings (required to publish).
3. Create an API token scoped to the account (or set up trusted publishing
   via GitHub Actions - better long-term: PyPI > Publishing > GitHub,
   owner sebin-gg, repo slowlang, workflow `publish.yml`, env `pypi`).
4. Build + upload from the repo root:
   ```
   python -m pip install build twine
   python -m build
   twine upload dist/*    # uploads `slowlang`
   ```
5. For `tortoiselang`: temporarily set `name = "tortoiselang"` in
   pyproject.toml, `python -m build`, upload, revert. (A second dist name
   for the same project is how the squat is claimed; PyPI treats them as
   independent names.)

## 2. npm (claim `slowlang`)

npm does NOT support Google SSO - use GitHub SSO (your stated fallback).

1. https://www.npmjs.com/signup - "Continue with GitHub" (account sebin-gg).
2. Verify email. Enable 2FA (npm requires it for publishing from CLI tokens).
3. From repo root: `npm login` (opens browser GitHub flow) then `npm publish`.
   The package is bin/slowlang.js - the joke CLI checker.

## 3. VS Code Marketplace

1. https://marketplace.visualstudio.com/manage - Microsoft account,
   create Azure DevOps org, publisher ID `sebin-gg`.
2. `npm i -g @vscode/vsce` and `vsce login sebin-gg` (needs a DevOps PAT,
   scope: Marketplace > Manage).
3. `cd editors/vscode && vsce package && vsce publish`.

## 4. Hugging Face static Space (free tier)

1. https://huggingface.co/join - GitHub SSO works.
2. New Space > SDK = "Static" > name `slowlang`.
3. Push the demo dir as the space root:
   `git clone https://huggingface.co/spaces/sebin-gg/slowlang` then copy
   `demo/*` in and push. Zero build config needed.

## 5. Posts only you can make

- Show HN - `promo/posts/show-hn.md` (HN account required, author in thread)
- Product Hunt - `promo/posts/product-hunt.md` (@sebin_gg)
- r/esolangs - `promo/posts/reddit-esolangs.md`
- r/SideProject + r/ProgrammerHumor - `promo/posts/reddit-sideproject.md`
- esoteric.codes email - `promo/posts/esoteric-codes-email.txt`
- Truttle1 (YouTube esolang reviews) - comment/DM him the repo + demo links
- 99-bottles-of-beer.net - submit a SlowLang entry on the site
- Open Hub (openhub.net) - claim the project page (GitHub OAuth works)
- HackerNoon - republish the DEV article via their editor
- PyCoder's Weekly - submit the blog URL via their form
