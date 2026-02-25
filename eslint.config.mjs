export default [
  {
    ignores: [
      '.venv/**',
      '.pytest_cache/**',
      '**/__pycache__/**',
      'node_modules/**',
      'reports/**',
      'test-results/**',
      '.husky/**',
    ],
  },
  {
    files: ['**/*.{js,cjs,mjs}'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
    },
    rules: {
      'no-undef': 'error',
      'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    },
  },
];
