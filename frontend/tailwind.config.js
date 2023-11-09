// ~/janus/frontend/tailwind.config.js

module.exports = {
  purge: [
    // Paths to all of your components' files
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './src/**/*.{js,ts,jsx,tsx}', // If this is where your Next.js components live
    '../../app/blueprints/**/templates/**/*.{html,js}', // Path to Flask templates
    '../../app/blueprints/**/static/**/*.{css,js}', // Path to Flask static assets
    // Add additional paths as your project grows
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}