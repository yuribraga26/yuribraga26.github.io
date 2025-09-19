# Yuri Braga - Portfolio Website

This repository contains the static files for Yuri Braga's professional portfolio website.

## 🚀 Live Website
Visit: [www.mryuribraga.com](https://www.mryuribraga.com)

## 📋 About
Professional portfolio showcasing expertise in:
- Automation and Machine Learning
- Healthcare AI (CareFuse)
- Embedded Systems and Firmware
- PCB Design and Robotics

## 🛠 Technology Stack
- Next.js 14 (Static Export)
- TypeScript
- Tailwind CSS
- Responsive Design

## 📁 Deployment
This site is deployed using GitHub Pages with the following structure:
- `index.html` - Main landing page
- `404.html` - Fallback for client-side routing
- `_next/` - Next.js static assets
- `images/` - Portfolio images and assets
- `CNAME` - Custom domain configuration

## 📧 Contact
- Email: yuri.braga@carefuseai.com
- LinkedIn: [linkedin.com/in/yuribraga1](https://linkedin.com/in/yuribraga1)
- CareFuse: [carefuseai.com](https://carefuseai.com)

## Run locally (npm)

If you want to preview this repository locally, there are two common approaches depending on whether you have the Next.js source (recommended) or only the built static files (this repo contains static output):

A) Quick static preview (this repository contains static HTML)

1. Install a small static file server (one-time):

```bash
npm install -g serve
```

2. From the repository root, run:

```bash
serve -s . -l 3000
```

3. Open http://localhost:3000 in your browser to preview the static site.

Notes:
- This serves the built static files exactly as they are in the repo (no rebuild step).
- Good for sanity checks and quick previews of `index.html` and other static pages.

B) Run from Next.js source (if you have the project source and `package.json`)

If you have the original Next.js project (source code and `package.json`), follow these steps in a terminal from the project root:

```bash
# install dependencies
npm install

# run the dev server
npm run dev

# or to build the static export
npm run build
npm run export

# then serve the `out/` folder (for example)
npx serve out -l 3000
```

Notes:
- Typical scripts in `package.json` are `dev`, `build`, and `export` for a statically-exported Next.js site.
- If your project uses `next export` you will get an `out/` directory with static files, which you can serve with the `serve` command above.
- If you only have the static output (this repo), the quick static preview in (A) is enough.

Troubleshooting
- If you still see old widgets or client-side behavior, clear your browser cache or try a hard reload (Ctrl+Shift+R). If the site is hosted behind a CDN, you may need to invalidate the cache there.
- To restore interactive features or produce a consistent client bundle, modify the Next.js source and run a full rebuild (`npm run build`), then redeploy the generated static output.

---
Built with ❤️ by Yuri Braga

