/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'dark-bg': '#0f0f0f',
        'dark-surface': '#1a1a1a',
        'dark-border': '#2a2a2a',
        'accent': '#3b82f6',
        'accent-hover': '#2563eb',
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

