Durable Next.js Source-level Rebuild

Goal

Provide a repeatable, source-level process to: remove the recommendation upload/manual UI, remove rating stars, update contact email, change CareFuse AUC to 0.93, and update coursework. Produce a fresh static export so the `_next` client bundles and serialized RSC payloads match the static HTML (durable fix).

Assumptions

- This repository currently contains only a Next.js static export (pre-built `index.html`, `_next/`, etc.).
- You have (or can obtain) the original Next.js project source (the repo that contains `package.json`, `app/` or `pages/`, and `next.config.js`).
- Rebuild will be run from WSL on Windows. Commands below use the WSL shell and assume Node.js >= 18.

High-level options

A) Recommended (if you have the Next.js source)
1. Clone the Next.js source repository (or `cd` to your local copy).
2. Edit source components (see "Files to edit" below).
3. Run `npm install` (or `pnpm install` / `yarn`).
4. Build and export: `npm run build` then `npm run export` (or project-specific scripts).
5. Verify the `out/` (or `exported` directory) static files. Replace the static files in this repo with the generated export.
6. Commit and deploy the exported static files.

B) Short-term fallback (if you don't have source)
- You can continue to neutralize the problematic runtime artifacts in this static export (we started that), but it's brittle and may be overwritten by any future rebuild. Prefer option A for a lasting fix.

Files to edit in the source (likely locations)

- app/recommendations/page.tsx (or pages/recommendations.tsx)
  - Remove or conditionally render out components that provide:
    - "Upload Recommendation Letter" file input
    - "Add Recommendation Manually" form
    - Rating selector / star visuals (remove the "5 Stars" option and star display)
  - Update static markup to include the Brewer recommendation block in the same format as the others.

- app/contact/page.tsx (or pages/contact.tsx)
  - Replace any hard-coded/JSON contact object containing the old email (e.g., `ybraga@vt.edu`) with `yuri.braga@carefuseai.com`.

- app/campus-involvement/page.tsx (or components) or wherever ECE Ambassadors role is stored
  - Set role to "President" (update the appropriate data file or component props).

- app/academics/page.tsx
  - Update "Key Coursework" to the user's exact ordered list:
    1) Artificial Intelligence Engineering
    2) Computer Systems
    3) Advanced Real-Time Systems
    4) Large Scale Software Design

- app/carefuse/page.tsx or a component/const containing the AUC value
  - Update AUC from 0.87 -> 0.93.

Backup & rollback plan

1. From the static-export repo (this repo), run the included backup script to snapshot `index.html`, the `_next/` directory, `images/`, and any HTML/json payload files: `./scripts/backup_static_export.sh`.
2. In the Next.js source repo, create a dedicated branch (e.g., `site-fix/remove-recommendation-ui`) and commit your edits.
3. Run `npm run build && npm run export` and verify the `out/` directory.
4. Replace the files in the static-export repo with the new `out/` contents. Keep the backup created in step 1.
5. If something goes wrong, restore the backup and open an issue in the source repo for follow-up.

Exact commands (WSL)

# Prepare WSL environment (one-time)
sudo apt update && sudo apt install -y build-essential curl git
# Install Node (if needed)
# Recommended Node version: 18.x or 20.x (LTS). If you use nvm, install and use it.

# Clone source (example - change to your source repo)
git clone git@github.com:yourusername/your-nextjs-site.git
cd your-nextjs-site

# Install dependencies (choose one based on your project)
npm install
# or
# pnpm install
# or
# yarn install

# Edit files (use your editor). Then build & export
npm run build
npm run export

# Serve the exported site for verification (from the source repo)
npx serve out -l 3000
# or copy `out/` into this static-export repository root (make a backup first)

Script to backup current static export (this repo)

We included `scripts/backup_static_export.sh` that:
- creates a `backups/<timestamp>/` directory
- copies `index.html`, `_next/`, `images/`, and all top-level route `*/index.html` files there

Usage (from repo root):

chmod +x scripts/backup_static_export.sh
./scripts/backup_static_export.sh

Estimated time & verification

- If you already have source and dependencies cached locally: ~10-30 minutes to edit, build, and export.
- If you need to fetch dependencies and edit multiple components: 30-90 minutes.
- Verification: start `npx serve out -l 3000` and test `/contact`, `/recommendations`, `/academics`, and `/carefuse`.

Next steps I can take for you (choose one):

1) If you provide the Next.js source (or a repo URL), I will edit the source files directly and run the build/export here in WSL, then replace the static export and verify locally.
2) If you want me to continue with the brittle but immediate static-export neutralization (find & patch remaining compiled chunks and payloads, update AUC), I can automate that across the repo and keep backups.
3) I can prepare a PR patch you can apply in your Next.js source repo with the exact code changes (recommended if you prefer to review edits in source form).

Pick an option and I will proceed. If you pick (1), please provide read access to the source or push it into this workspace. If you pick (3), tell me whether you prefer a single commit/PR patch or a set of smaller commits.
