/** @type {import('validate-branch-name').Config} */
const config = {
  pattern: /^(feat|fix|docs|style|refactor|perf|test|chore|ci|revert)\/([a-z0-9-]+)$/,
  errorMsg:
    '❌ [BRANCH LINT ERROR] Branch name outside the Enterprise standard!\n' +
    '💡 Use the format: <type>/<short-description-in-kebab-case>\n' +
    '📌 Example: feat/linear-regression-byd\n' +
    '🚀 Allowed types: feat, fix, docs, style, refactor, perf, test, chore, ci, revert',
};

export default config;
