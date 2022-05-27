module.exports = {
  content: ["./_site/**/*.*"],
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
