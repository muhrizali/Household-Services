/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../templates/*.{html,js}",
    "../templates/**/*.{html,js}",
  ],
  theme: {
    extend: {
      fontFamily: {
        fira: ["Fira Sans",],
      }
    },
  },
  plugins: [
    require('daisyui'),
  ],
  daisyui: {
    themes: [
      {
        "mali-light": {
          "primary": "#818cf8",
          "primary-content": "#060715",

          "secondary": "#22d3ee",
          "secondary-content": "#001014",

          "accent": "#e879f9",
          "accent-content": "#130515",

          "neutral": "#e5e5e5",
          "neutral-content": "#121212",

          "base-100": "#f3f4f6",
          "base-200": "#d3d4d6",
          "base-300": "#b4b5b7",
          "base-content": "#141415",

          "info": "#60a5fa",
          "info-content": "#030a15",

          "success": "#4ade80",
          "success-content": "#021206",

          "warning": "#facc15",
          "warning-content": "#150f00",

          "error": "#f87171",
          "error-content": "#150404",
        }
      },
    ]
  }
}

