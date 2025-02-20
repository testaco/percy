const chokidar = require('chokidar');
const fs = require('fs').promises;
const path = require('path');

// Config
const OUTPUTS_DIR = '../outputs';
const DATA_DIR = 'data';
const LEADERBOARD_FILE = path.join(DATA_DIR, 'leaderboard.json');

// Ensure directory exists
async function ensureDir(dir) {
  try {
    await fs.access(dir);
  } catch {
    console.log(`Creating directory: ${dir}`);
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
    if (result && result.summary && result.summary.score !== undefined) {
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
    } else {
      console.warn(`Skipping invalid result file: ${file} - missing required fields`);
    }
  }

  return {
    last_updated: new Date().toISOString(),
    results
  };
}

// Initialize watcher
async function init() {
  try {
    // Validate and ensure directories exist
    const outputsPath = path.resolve(OUTPUTS_DIR);
    const dataPath = path.resolve(DATA_DIR);

    // Check if outputs directory exists
    try {
      await fs.access(outputsPath);
      console.log(`Monitoring directory: ${outputsPath}`);
    } catch (err) {
      console.error(`Error: Outputs directory does not exist: ${outputsPath}`);
      console.error('Please create the outputs directory and try again');
      process.exit(1);
    }

    // Ensure data directory exists
    await ensureDir(dataPath);
    
    // Handle file changes
    async function handleChange() {
      try {
        const files = await fs.readdir(outputsPath);
        const jsonFiles = files
          .filter(f => f.endsWith('.json'))
          .map(f => path.join(outputsPath, f));
        
        const leaderboard = await aggregateResults(jsonFiles);
        await fs.writeFile(LEADERBOARD_FILE, JSON.stringify(leaderboard, null, 2));
        
        console.log(`Updated leaderboard.json at ${new Date().toISOString()}`);
      } catch (err) {
        console.error('Error updating leaderboard:', err);
        // Don't exit on update errors - keep watching
      }
    }

    // Set up watcher with error handling
    const watcher = chokidar.watch(outputsPath, {
      ignored: /(^|[\/\\])\../, // ignore dotfiles
      persistent: true,
      awaitWriteFinish: {
        stabilityThreshold: 2000,
        pollInterval: 100
      }
    });

    // Watch for changes
    watcher
      .on('add', handleChange)
      .on('change', handleChange)
      .on('unlink', handleChange)
      .on('error', error => {
        console.error('Watcher error:', error);
      });

    // Do initial aggregation
    await handleChange();
    
    console.log('Watching outputs directory for changes...');

    // Keep the process alive
    process.on('SIGINT', () => {
      console.log('Stopping watcher...');
      watcher.close().then(() => process.exit(0));
    });

  } catch (err) {
    console.error('Fatal error:', err);
    process.exit(1);
  }
}

// Start the watcher
init().catch(err => {
  console.error('Failed to start watcher:', err);
  process.exit(1);
});
