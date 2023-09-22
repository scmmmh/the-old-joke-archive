/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/app.css',
    './src/**/*.svelte',
  ],
  theme: {
    extend: {
      padding: {
        'vw-2': '0.5vw',
        'vw-8': '2vw',
      },
      colors: {
        primary: '#814158',
        accent: '#2d8095',
      },
      borderWidth: {
        px: '1px',
      },
      fontFamily: {
        'blackriver-bold': 'blackriver-bold, serif',
        'merriweather-regular': 'Merriweather-Regular, serif',
        'merriweather-italic': 'Merriweather-Italic, serif',
        'merriweather-bold': 'Merriweather-Bold, serif',
        'merriweather-bold-italic': 'Merriweather-BoldItalic, serif',
      },
      outline: {
        primary: '2px solid #814158',
      },
      maxWidth: {
        '9/10': '90%',
      },
      maxHeight: {
        '9/10': '90%',
      },
      width: {
        '9/10-screen': '90vw',
      },
      height: {
        '9/10-screen': '90vh',
      },
      zIndex: {
        'dialog': '1000',
      }
    },
  },
  plugins: [],
}
