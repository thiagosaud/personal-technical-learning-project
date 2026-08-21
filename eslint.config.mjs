// @ts-check
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import sonarjs from 'eslint-plugin-sonarjs';
import security from 'eslint-plugin-security';
import unicorn from 'eslint-plugin-unicorn';
import eslintConfigPrettier from 'eslint-config-prettier';
import { fixupConfigRules } from '@eslint/compat';
import { defineConfig } from 'eslint/config';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const TS_FILES = ['**/*.{ts,tsx}'];
const ALL_JS_AND_TS_FILES = ['**/*.{js,mjs,cjs,ts,tsx}'];

export default defineConfig([
  // ==========================================
  // 1. GLOBAL IGNORES
  // ==========================================
  {
    ignores: [
      '**/node_modules/**',
      '**/dist/**',
      '**/build/**',
      '**/out/**',
      '**/.venv/**',
      '**/coverage/**',
      '**/.next/**',
    ],
  },

  // ==========================================
  // 2. THIRD-PARTY PLUGINS & PRESETS
  // ==========================================
  js.configs.recommended,

  .../** @type {any} */ (
    fixupConfigRules(
      // @ts-expect-error - Suppresses ecosystem version typing discrepancies
      security.configs.recommended
    )
  ),

  .../** @type {any[]} */ (
    Array.isArray(unicorn.configs['recommended']) ? unicorn.configs['recommended'] : [unicorn.configs['recommended']]
  ),

  .../** @type {any[]} */ (
    Array.isArray(sonarjs?.configs?.recommended)
      ? sonarjs.configs.recommended
      : [sonarjs?.configs?.recommended ?? sonarjs]
  ),

  // ==========================================
  // 3. TYPESCRIPT ENVIRONMENT PRESETS (Strictly bound to TS files)
  // ==========================================
  // By isolating strict type rule injection to TS_FILES only, we completely
  // eliminate the projectService parsing engine loop crashes on loose config files.
  ...tseslint.configs.strictTypeChecked.map((config) => ({
    ...config,
    files: TS_FILES,
  })),
  ...tseslint.configs.stylisticTypeChecked.map((config) => ({
    ...config,
    files: TS_FILES,
  })),

  // ==========================================
  // 4. SHARED PROJECT APPLICATION RULES (Universal)
  // ==========================================
  {
    files: ALL_JS_AND_TS_FILES,
    languageOptions: {
      globals: {
        process: 'readonly',
        console: 'readonly',
        Buffer: 'readonly',
        setTimeout: 'readonly',
        clearTimeout: 'readonly',
        setInterval: 'readonly',
        clearInterval: 'readonly',
        __dirname: 'readonly',
        __filename: 'readonly',
      },
    },
    rules: {
      'no-console': ['warn', { allow: ['warn', 'error', 'log', 'info'] }],
      'prefer-const': 'error',
      'no-unused-vars': 'off',
      'unicorn/prevent-abbreviations': 'off',
      'sonarjs/cognitive-complexity': ['error', 15],
      'sonarjs/no-duplicate-string': 'warn',
    },
  },

  // ==========================================
  // 5. TYPESCRIPT ONLY COMPILER SERVICE
  // ==========================================
  {
    files: TS_FILES,
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        projectService: true,
        tsconfigRootDir: __dirname,
      },
    },
    rules: {
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/await-thenable': 'error',
      '@typescript-eslint/no-floating-promises': 'error',
    },
  },

  // ==========================================
  // 6. AUTOMATION SCRIPTS OVERRIDES (Safe Execution Layer)
  // ==========================================
  {
    files: [
      'scripts/**/*.{js,mjs,cjs}',
      '**/scripts/**/*.{js,mjs,cjs}',
      '*.config.{js,mjs,cjs}',
      '**/*.config.{js,mjs,cjs}',
      '.prettierrc.mjs',
    ],
    rules: {
      'unicorn/no-process-exit': 'off',
      'no-console': 'off',
      'no-undef': 'off',
      'sonarjs/no-os-command-from-path': 'off',
      'security/detect-unsafe-regex': 'off',
      'security/detect-non-literal-regexp': 'off',
      'unicorn/no-declarations-before-early-exit': 'off',
    },
  },

  // ==========================================
  // 7. TEST FILE ENVIRONMENT OVERRIDES
  // ==========================================
  {
    files: ['**/*.{test,spec}.{ts,js}'],
    rules: {
      '@typescript-eslint/no-explicit-any': 'off',
      'sonarjs/no-identical-functions': 'off',
    },
  },

  // ==========================================
  // 8. FORMATTING PROTECTION (Always Last)
  // ==========================================
  eslintConfigPrettier,
]);
