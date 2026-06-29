# Resume PDF Update Guide

This repository is a static export, so the live resume download is served from the deployed path configured in `site-config.json`.

Current canonical path:
`/resume/Yuri_Braga_Resume.pdf`

## Workflow A: Replace the file in place

1. Replace `resume/Yuri_Braga_Resume.pdf` with the new PDF.
2. Keep the filename the same.
3. No code changes are needed.

This is the safest workflow because every resume link already points to that canonical filename.

## Workflow B: Use a new filename

1. Place the new PDF in `resume/`.
2. Update `resumePdfPath` in `site-config.json`.
3. Update any visible resume link labels if you want the text to change.

## Recommended command

Run this from the repository root:

```bash
node scripts/update-resume.js /local/path/to/new-resume.pdf
```

What the script does:

- Validates that the input file exists.
- Confirms that the file is a PDF.
- Copies the PDF to `resume/Yuri_Braga_Resume.pdf`.
- Mirrors the same file to `public/resume/Yuri_Braga_Resume.pdf` for a future source-tree workflow.

If you later restore a Next.js source tree, import the same resume path from the shared config instead of hardcoding the filename in page components.
