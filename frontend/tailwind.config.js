// Import your design tokens
const colors = require('./src/design-tokens/colors');
const typography = require('./src/design-tokens/typography');
const spacing = require('./src/design-tokens/spacing');

module.exports = {
  purge: ['./pages/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  darkMode: `class`, // or 'media' or false
  theme: {
    extend: {
      colors: {
        // Spread the colors from your tokens here
        ...colors,
      },
      fontSize: {
        // Spread the font sizes from your tokens here
        ...typography.fontSizes,
      },
      fontWeight: {
        // Spread the font weights from your tokens here
        ...typography.fontWeights,
      },
      spacing: {
        // Spread the spacing values from your tokens here
        ...spacing,
      },
      // Add any other token categories you've defined
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
