const icons = {
  sizes: {
    // Adjusting size names to reflect their application context
    compact: '1em', // Use for tighter spaces or alongside small text
    default: '1.5em', // Standard size for most use cases
    prominent: '2em', // Larger, for when icons need to be more prominent
    // Consider adding an extra size for very large icons used in hero sections or as major navigational elements
    hero: '3em',
  },
  colors: {
    // Adding color tokens for icons to enhance flexibility
    primary: 'var(--color-primary)', // Primary brand color
    secondary: 'var(--color-secondary)', // Secondary color
    action: 'var(--color-accent)', // For interactive icons
    muted: 'var(--color-mediumGray)', // Less emphasis, for background icons or disabled states
  },
  lineWeights: {
    // Adding line weight tokens for scalable vector icons, ensuring visual consistency
    thin: '1px',
    normal: '2px', // Default line weight for most icons
    thick: '3px', // For icons that require more visual weight
  },
  // Additional properties can be included here, such as different shapes, rounded corners, or specific animation tokens for interactive icons
};
