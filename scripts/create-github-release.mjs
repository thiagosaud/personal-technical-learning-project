import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';

const packageJson = JSON.parse(readFileSync('package.json', 'utf8'));
const currentVersion = packageJson.version;

let previousVersion;

try {
  const previousPackageJson = JSON.parse(
    execFileSync('git', ['show', 'HEAD^:package.json'], {
      encoding: 'utf8',
    })
  );

  previousVersion = previousPackageJson.version;
} catch {
  console.log('No parent package.json found; skipping release creation.');
  process.exit(0);
}

if (currentVersion === previousVersion) {
  console.log('Package version did not change; skipping release creation.');
  process.exit(0);
}

if (!/^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$/.test(currentVersion)) {
  console.error(`Invalid package version: ${currentVersion}`);
  process.exit(1);
}

const tag = `v${currentVersion}`;
const isPrerelease = currentVersion.includes('-');

try {
  execFileSync('gh', ['release', 'view', tag], {
    stdio: 'ignore',
  });

  console.log(`Release ${tag} already exists; skipping.`);
  process.exit(0);
} catch {
  // The release does not exist yet.
}

const releaseArguments = [
  'release',
  'create',
  tag,
  '--target',
  process.env.GITHUB_SHA || 'HEAD',
  '--title',
  tag,
  '--generate-notes',
];

if (isPrerelease) {
  releaseArguments.push('--prerelease');
}

execFileSync('gh', releaseArguments, {
  stdio: 'inherit',
});

console.log(`GitHub Release ${tag} created successfully.`);
