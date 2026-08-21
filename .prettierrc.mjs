/**
 * Global Monorepo Prettier Configuration Engine.
 * Official Documentation Reference: https://prettier.io
 *
 * @type {import("prettier").Config}
 */
const config = {
  semi: true, // Enforces semi-colons at the end of every executable statement
  singleQuote: true, // Uses single quotes instead of double quotes across JS/TS source files
  trailingComma: 'es5', // Trailing commas where valid in ES5 (objects, arrays, etc.) to keep clean git diffs
  printWidth: 120, // Limits line lengths to 120 characters to ensure clean modern multi-window monitor layout readability
  tabWidth: 2, // Slipped block layout aligned explicitly with your root .editorconfig policies
  useTabs: false,
  bracketSpacing: true, // Maintains spatial padding layout inside object literal destructuring brackets
};

export default config;
