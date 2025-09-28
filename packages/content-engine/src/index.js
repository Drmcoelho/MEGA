const fs = require('fs');
const path = require('path');
const YAML = require('yaml');

function parseModule(dir) {
  const manifestPath = path.join(dir, 'manifest.yaml');
  if (!fs.existsSync(manifestPath)) return null;
  const raw = fs.readFileSync(manifestPath, 'utf-8');
  const manifest = YAML.parse(raw);
  const lessonsDir = path.join(dir, 'lessons');
  let lessons = [];
  if (fs.existsSync(lessonsDir)) {
    lessons = fs.readdirSync(lessonsDir).filter(f => f.endsWith('.md'));
  }
  return { ...manifest, lessons };
}

module.exports = { parseModule };