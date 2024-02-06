const border = {
  width: {
    // Refining semantic naming based on use rather than purely descriptive
    default: '1px', // Default border width for most UI elements
    focus: '2px', // Highlighted or focused elements, slightly thicker
    interactive: '3px', // Borders for interactive elements like buttons or clickable cards
  },
  style: {
    // Styles remain largely descriptive but are crucial for semantic usage
    solid: 'solid', // Most common border style for clarity and emphasis
    dashed: 'dashed', // Used for indicating boundaries that are not continuously connected or for decorative purposes
    dotted: 'dotted', // Used for subtle separations or to indicate a less permanent boundary
  },
  radius: {
    // Semantic naming reflecting potential use cases
    none: '0px', // No radius for square borders
    subtle: '4px', // Slightly rounded corners for a soft appearance
    standard: '8px', // Standard border radius for moderate rounding, suitable for cards, buttons, etc.
    pill: '16px', // Highly rounded edges for pill-shaped elements
    circular: '50%', // Full circle for round elements like avatars or icons
  },
  color: {
    // Incorporating border colors with a semantic approach, assuming color tokens are defined elsewhere
    primary: 'var(--color-primary)', // Primary brand color for emphasis
    secondary: 'var(--color-secondary)', // Secondary color for less emphasis
    accent: 'var(--color-accent)', // Accent color for interactive or focus elements
    muted: 'var(--color-mediumGray)', // Muted color for subtle borders
  },
};
