import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..');

// 1. Read index.html and extract the cls() function
const htmlPath = path.join(rootDir, 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const match = html.match(/const cls\s*=\s*([^;]+);/);

assert.ok(match, 'Could not locate `const cls = ...` in index.html');
const clsFnStr = match[1];
// eslint-disable-next-line no-eval
const cls = eval(`(${clsFnStr})`);

// 2. Define the exact test values from the prompt:
// 0, 10, 11, 25, 26, 60, 61, 99, 100 and a dead tree
const testDefolValues = [0, 10, 11, 25, 26, 60, 61, 99, 100];

// Expected ICP Forests classes:
// 0 (0-10%), 1 (11-25%), 2 (26-60%), 3 (61-99%), 4 (dead / 100%)
const jsResults = testDefolValues.map(defol => ({
  defol,
  dead: false,
  cls: cls({ defol, dead: false })
}));

// Test dead tree (with arbitrary defoliation, e.g. 30%)
const jsDeadResult = {
  defol: 30,
  dead: true,
  cls: cls({ defol: 30, dead: true })
};

// 3. Obtain Python results from betulog.icp.defol_class
let pythonBin = process.platform === 'win32' && fs.existsSync(path.join(rootDir, '.venv', 'Scripts', 'python.exe'))
  ? path.join(rootDir, '.venv', 'Scripts', 'python.exe')
  : (process.env.VIRTUAL_ENV ? path.join(process.env.VIRTUAL_ENV, 'bin', 'python') : 'python3');

let pyOutput;
try {
  pyOutput = execSync(
    `"${pythonBin}" -c "import json; from betulog import defol_class; vals = [0, 10, 11, 25, 26, 60, 61, 99, 100]; res = [int(x) for x in defol_class(vals)]; res.append(int(defol_class(30, dead=True))); print(json.dumps(res))"`,
    { cwd: rootDir, encoding: 'utf8' }
  );
} catch {
  // Fallback to 'python' if python3 is unavailable
  pythonBin = 'python';
  pyOutput = execSync(
    `"${pythonBin}" -c "import json; from betulog import defol_class; vals = [0, 10, 11, 25, 26, 60, 61, 99, 100]; res = [int(x) for x in defol_class(vals)]; res.append(int(defol_class(30, dead=True))); print(json.dumps(res))"`,
    { cwd: rootDir, encoding: 'utf8' }
  );
}

const pyResults = JSON.parse(pyOutput.trim());
const expectedClasses = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4];

console.log('Testing JS index.html vs Python betulog.defol_class parity:');
testDefolValues.forEach((val, idx) => {
  const jsCls = jsResults[idx].cls;
  const pyCls = pyResults[idx];
  const expCls = expectedClasses[idx];
  console.log(`  defol = ${val.toString().padStart(3, ' ')}%: JS = ${jsCls}, Python = ${pyCls}, Expected = ${expCls}`);
  assert.strictEqual(jsCls, expCls, `JS mismatch for defol=${val}`);
  assert.strictEqual(pyCls, expCls, `Python mismatch for defol=${val}`);
  assert.strictEqual(jsCls, pyCls, `Parity failure between JS and Python for defol=${val}`);
});

console.log(`  dead tree (defol=30%, dead=true): JS = ${jsDeadResult.cls}, Python = ${pyResults[9]}, Expected = 4`);
assert.strictEqual(jsDeadResult.cls, 4, 'JS mismatch for dead tree');
assert.strictEqual(pyResults[9], 4, 'Python mismatch for dead tree');
assert.strictEqual(jsDeadResult.cls, pyResults[9], 'Parity failure for dead tree');

console.log('\nAll parity checks passed successfully!');
