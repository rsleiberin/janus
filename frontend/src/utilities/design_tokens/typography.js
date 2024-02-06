const typography = {
  fonts: {
    primary: "'Roboto', sans-serif", // Primary font for body text
    secondary: "'Orbitron', sans-serif", // Secondary font for headings and accents
    // Consider adding a tertiary or a functional font for monospaced uses like code if needed.
  },
  fontSizes: {
    // Using a semantic approach for different roles
    tiny: '0.6875rem', // For less important, small text
    small: '0.875rem', // Small text
    body: '1rem', // Default body text size
    large: '1.125rem', // Larger text that's not quite a heading
    headingSmall: '1.5rem', // Small headings
    headingMedium: '2rem', // Medium headings
    headingLarge: '2.5rem', // Large headings
    headingXLarge: '3rem', // Extra large headings
  },
  fontWeights: {
    light: 300, // Light weight for delicate emphasis
    normal: 400, // Default text weight
    medium: 500, // Medium emphasis
    bold: 700, // Bold text for high emphasis
    extraBold: 900, // Extra bold for maximum emphasis
  },
  lineHeights: {
    tight: 1.2, // Tight line height for headings
    normal: 1.5, // Default line height for body text
    relaxed: 1.75, // Relaxed line height for more readable, longer text
  },
  // Adding letter spacing tokens can also be beneficial for certain typographic styles
  letterSpacing: {
    normal: 'normal', // Default letter spacing
    expanded: '0.05em', // Expanded spacing for headings/caps
  },
};
