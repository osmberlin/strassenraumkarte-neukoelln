module.exports = {
  mode: 'jit',
  purge: [
    './_includes/**/*.*',
    './_layouts/**/*.*',
    './_posts/**/*.*',
    './javascript/**/*.js',
    './parkraumkarte/**/*.js',
    './posts/**/*.js',
    './*.md',
    './*.html',
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
