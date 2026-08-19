import packageJson from '../package.json' with { type: 'json' };

const config = packageJson['validate-branch-name'];
const branchName = process.env.BRANCH_NAME;

if (!config) {
  console.error('validate-branch-name configuration is missing from package.json.');
  process.exit(1);
}

if (!branchName) {
  console.error('BRANCH_NAME is required.');
  process.exit(1);
}

const branchPattern = new RegExp(config.pattern);

if (!branchPattern.test(branchName)) {
  console.error(config.errorMsg);
  process.exit(1);
}

console.log(`Branch name validation passed: ${branchName}`);
