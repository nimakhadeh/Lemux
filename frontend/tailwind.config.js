/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        persian: {
          blue: '#1d4ed8',
          green: '#00a693',
          red: '#c81e1e',
          gold: '#d4af37'
        }
      },
      fontFamily: {
        'sans': ['Vazir', 'Tahoma', 'Arial', 'sans-serif'],
      },
      direction: 'rtl', // پشتیبانی از راست به چپ
    },
  },
  plugins: [],
}