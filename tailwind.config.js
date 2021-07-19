module.exports = {
  mode: 'jit',
  purge: [
    './_includes/**/*.*',
    './_layouts/**/*.*',
    './_posts/**/*.*',
    './javascript/**/*.js',
    './parkraumkarte/**/*.js',
    './posts/**/*.js',
    './parkraumkarte/report.md',
    './parkraumkarte/data.html',
    './*.md',
    './*.html',
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      screens: {
        'print': { 'raw': 'print' },
      },
      zIndex: {
        '1000': '1000'
      },
      // colors: {
      //   map: {
      //     purple: '#7D5197',
      //   }
      // },
      // typography: {
      //   DEFAULT: {
      //     css: {
      //       h1: {
      //         color: '#7D5197',
      //       }
      //     },
      //   },
      // },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
}
