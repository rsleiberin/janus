// Border Token File
// This file defines border tokens used across the design system.
// Border tokens are crucial for maintaining visual consistency and clarity in the UI.

const borderToken = {
    // Border Width: Defines the thickness of the borders.
    // Use different widths to indicate the importance or interactivity of elements.
    borderWidth: {
      thin: '1px',      // For subtle borders where emphasis is low.
      medium: '2px',    // Default border width for standard UI elements.
      thick: '3px'      // For elements that require more visual weight.
    },
  
    // Border Style: Defines the style of the borders (solid, dotted, dashed, etc.).
    // Different styles can be used for various visual cues or aesthetic preferences.
    borderStyle: {
      solid: 'solid',   // Most common, used for clear and defined edges.
      dotted: 'dotted', // For a less pronounced boundary, often used for hints or secondary elements.
      dashed: 'dashed'  // For intermediate emphasis, can indicate something editable or changeable.
    },
  
    // Border Color: Aligns with the color scheme of the design system.
    // Color choice can impact the visibility and emphasis of the borders.
    borderColor: {
      primary: '#007bff', // Primary brand color for emphasis.
      secondary: '#6c757d', // Secondary color for less emphasis.
      muted: '#ced4da' // Muted color for subtle borders.
    }
  };
  
  // Export the borderToken for consistent use across the design system.
  // Consistency in border styles enhances the user experience by providing a clear and organized visual structure.
  export default borderToken;
  