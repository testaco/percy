const chokidar = require('chokidar');
const fs = require('fs').promises;
const path = require('path');

// Config
const OUTPUTS_DIR = '../../outputs';
const DATA_DIR = '../data';
const LEADERBOARD_FILE = path.join(DATA_DIR, 'leaderboard.json');

// Ensure data directory exists
async function ensureDir(dir) {
  try {
    await fs.access(dir);
  } catch {
    await fs.mkdir(dir, { recursive: true });
  }
}

// Load and parse a JSON file
async function loadJson(filepath) {
  try {
    const data = await fs.readFile(filepath, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    console.error(`Error loading ${filepath}:`, err);
    return null;
  }
}

// Aggregate test results into leaderboard data
async function aggregateResults(files) {
  const results = [];
  
  for (const file of files) {
    const result = await loadJson(file);
    if (result) {
      results.push({
        model: result.model,
        provider: result.provider,
        license_class: result.license_class,
        test_id: result.test_id,
        score: result.summary.score,
        passed: result.summary.passed,
        timestamp: result.timestamp,
        use_cot: result.use_cot,
        use_rag: result.use_rag,
        temperature: result.temperature
      });
    }
  }

  return {
    last_updated: new Date().toISOString(),
    results
  };
}

// Initialize watcher
async function init() {
  await ensureDir(DATA_DIR);
  
  // Watch the outputs directory
  const watcher = chokidar.watch(OUTPUTS_DIR, {
    ignored: /(^|[\/\\])\../, // ignore dotfiles
    persistent: true
  });

  // Handle file changes
  async function handleChange() {
    try {
      const files = await fs.readdir(OUTPUTS_DIR);
      const jsonFiles = files
        .filter(f => f.endsWith('.json'))
        .map(f => path.join(OUTPUTS_DIR, f));
      
      const leaderboard = await aggregateResults(jsonFiles);
      await fs.writeFile(LEADERBOARD_FILE, JSON.stringify(leaderboard, null, 2));
      
      console.log('Updated leaderboard.json');
    } catch (err) {
      console.error('Error updating leaderboard:', err);
    }
  }

  // Watch for changes
  watcher
    .on('add', handleChange)
    .on('change', handleChange)
    .on('unlink', handleChange);

  console.log('Watching outputs directory for changes...');
}

init().catch(console.error);
