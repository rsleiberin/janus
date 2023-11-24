const animations = {
  durations: {
    fast: '200ms',  // For quick transitions
    medium: '500ms', // Standard duration
    slow: '1000ms',  // For more noticeable transitions
  },
  easing: {
    linear: 'linear',
    easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
    easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
    easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
  },
  types: {
    hoverEffect: 'hover',  // For hover effects on elements
    morphing: 'morph',     // For blending shapes or images
    anthropomorphic: 'human-like', // For animations mimicking human movements
    kineticTypography: 'text-motion', // For moving text animations
    // Additional animation types as needed
  },
  // Add additional properties as needed for nuanced animations
};

export default animations;
