/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./*.html",
    "./rankings/*.html",
    "./restaurants/*.html",
    "./components/*.html",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['DM Sans', 'sans-serif'],
        poppins: ['Poppins', 'sans-serif'],
      },
      colors: {
        brand: {
          orange: '#E67E22',
          cream: '#FFF8F0',
          dark: '#2D3748',
          gray: '#4A4A4A',
        },
      },
    },
  },
  plugins: [],
}
