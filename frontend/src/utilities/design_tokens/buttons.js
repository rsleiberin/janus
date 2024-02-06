const buttons = {
  sizes: {
    // Using role-based naming for button sizes
    compact: {
      fontSize: '0.875rem', // Slightly smaller, for less prominent actions
      padding: '0.5rem 1rem',
    },
    default: {
      fontSize: '1rem', // The standard button size for most use cases
      padding: '0.75rem 1.5rem',
    },
    expansive: {
      fontSize: '1.25rem', // Larger, for primary actions requiring prominence
      padding: '1rem 2rem',
    },
  },
  styles: {
    // Defining button styles based on their intent
    action: {
      backgroundColor: '#333', // Dark for primary actions
      color: 'white',
      border: 'none',
    },
    outline: {
      backgroundColor: 'transparent',
      color: '#333', // Dark text for contrast on light backgrounds
      border: '1px solid #333', // Outlined style for secondary actions
    },
    muted: {
      backgroundColor: 'transparent',
      color: '#777', // Muted color for less important or destructive actions
      border: 'none',
    },
    // Additional style for disabled buttons could be added for completeness
    disabled: {
      backgroundColor: '#ccc',
      color: '#f9f9f9',
      border: 'none',
      opacity: '0.5',
      cursor: 'not-allowed',
    },
  },
};
