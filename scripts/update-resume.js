#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const repoRoot = path.resolve(__dirname, '..');
const configPath = path.join(repoRoot, 'site-config.json');

function readJson(filePath) {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function fail(message) {
    console.error(message);
    process.exit(1);
}

function isPdf(filePath) {
    const fileHandle = fs.openSync(filePath, 'r');
    try {
        const header = Buffer.alloc(5);
        const bytesRead = fs.readSync(fileHandle, header, 0, 5, 0);
        return bytesRead === 5 && header.toString('utf8') === '%PDF-';
    } finally {
        fs.closeSync(fileHandle);
    }
}

const sourcePath = process.argv[2];
if (!sourcePath) {
    fail('Usage: node scripts/update-resume.js <path-to-new-resume.pdf>');
}

const resolvedSourcePath = path.resolve(process.cwd(), sourcePath);
if (!fs.existsSync(resolvedSourcePath)) {
    fail(`Source file not found: ${resolvedSourcePath}`);
}

if (path.extname(resolvedSourcePath).toLowerCase() !== '.pdf' || !isPdf(resolvedSourcePath)) {
    fail(`Input file is not a valid PDF: ${resolvedSourcePath}`);
}

const config = readJson(configPath);
const resumePdfPath = typeof config.resumePdfPath === 'string' && config.resumePdfPath.trim()
    ? config.resumePdfPath.trim()
    : '/resume/Yuri_Braga_Resume.pdf';

const resumeFileName = path.basename(resumePdfPath);
const staticExportDestination = path.join(repoRoot, 'resume', resumeFileName);
const sourceTreeDestination = path.join(repoRoot, 'public', 'resume', resumeFileName);

for (const destinationPath of [staticExportDestination, sourceTreeDestination]) {
    fs.mkdirSync(path.dirname(destinationPath), { recursive: true });
    fs.copyFileSync(resolvedSourcePath, destinationPath);
}

console.log(`Updated resume PDF from ${resolvedSourcePath}`);
console.log(`Static export copy: ${staticExportDestination}`);
console.log(`Source-tree mirror: ${sourceTreeDestination}`);
console.log(`Served URL: ${resumePdfPath}`);
console.log('Deployment note: commit both resume/Yuri_Braga_Resume.pdf and public/resume/Yuri_Braga_Resume.pdf before pushing, otherwise GitHub Pages or a future Next build can still serve a stale/404 resume.');
