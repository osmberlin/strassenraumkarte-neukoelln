import { defineConfig } from 'oxlint'

export default defineConfig({
  jsPlugins: ['eslint-plugin-astro'],
  env: {
    builtin: true,
  },
  rules: {
    'eslint/no-unused-vars': 'off',
    'astro/missing-client-only-directive-value': 'error',
    'astro/no-conflict-set-directives': 'error',
    'astro/no-deprecated-astro-canonicalurl': 'error',
    'astro/no-deprecated-astro-fetchcontent': 'error',
    'astro/no-deprecated-astro-resolve': 'error',
    'astro/no-deprecated-getentrybyslug': 'error',
    'astro/no-unused-define-vars-in-style': 'error',
    'astro/valid-compile': 'error',
  },
  overrides: [
    {
      files: ['*.astro', '**/*.astro'],
      globals: { Fragment: 'readonly' },
      env: { astro: true, node: true },
    },
    {
      files: ['**/*.{jsx,tsx}'],
      rules: {
        'react-compiler/react-compiler': 'error',
      },
      jsPlugins: ['eslint-plugin-react-compiler'],
    },
  ],
})
