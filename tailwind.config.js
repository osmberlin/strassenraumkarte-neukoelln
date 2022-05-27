module.exports = {
  content: [
    "./_includes/**/*.*",
    "./_layouts/**/*.*",
    "./_posts/**/*.*",
    "./javascript/**/*.js",
    "./parkraumkarte/**/*.js",
    "./posts/**/*.js",
    "./parkraumkarte/report.md",
    "./parkraumkarte/data.html",
    "./*.md",
    "./*.html",
  ],
  theme: {
    extend: {
      zIndex: {
        1000: "1000",
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/typography"),
    require("@tailwindcss/aspect-ratio"),
  ],
};
