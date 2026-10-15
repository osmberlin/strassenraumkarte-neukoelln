/** @type {import("prettier").Config} */
export default {
  semi: false,
  singleQuote: true,
  arrowParens: 'always',
  printWidth: 100,
  plugins: [
    'prettier-plugin-astro',
    'prettier-plugin-organize-imports',
    'prettier-plugin-tailwindcss',
    'prettier-plugin-astro-organize-imports',
  ],
  overrides: [
    {
      files: '*.astro',
      options: {
        parser: 'astro',
      },
    },
  ],
  tailwindFunctions: ['clsx', 'twMerge', 'twJoin'],
  tailwindAttributes: ['className', 'class:list', 'class', 'sectionClasses'],
}
