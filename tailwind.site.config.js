/** Theme values copied from the previous Tailwind Play CDN config. */
module.exports = {
  content: [
    "./index.html",
    "./merci.html",
    "./confidentialite.html",
    "./proprietes.html",
    "./ca/**/*.html",
    "./assets/js/**/*.js",
    "./scripts/generate_property_pages.py",
  ],
  theme: {
    extend: {
      colors: {
        fred: {
          blue: "#282e64",
          gold: "#be9018",
          gray: "#F5F7FA",
        },
      },
      fontFamily: {
        sans: ["Montserrat", "sans-serif"],
      },
      letterSpacing: {
        luxury: "0.2em",
      },
      opacity: {
        98: ".98",
      },
    },
  },
  plugins: [],
};
