const animations = {
  durations: {
    instant: '100ms', // For immediate effects, slightly more perceptible than instant
    fast: '200ms',  // For quick transitions, good for subtle effects
    normal: '500ms', // Standard duration, balanced for most animations
    slow: '800ms',  // For slower, more noticeable transitions
    deliberate: '1200ms',  // For dramatic emphasis or complex animations
  },
  easing: {
    linear: 'linear', // Even speed throughout
    easeIn: 'cubic-bezier(0.4, 0, 1, 1)', // Accelerating from zero velocity
    easeOut: 'cubic-bezier(0, 0, 0.2, 1)', // Decelerating to zero velocity
    easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)', // Acceleration until halfway, then deceleration
    spring: 'cubic-bezier(0.34, 1.56, 0.64, 1)', // Mimics the movement of a spring for dynamic interactions
  },
  types: {
    fadeInOut: 'fade',  // For elements to fade in or out
    slideInOut: 'slide', // For elements to slide in or out, can specify direction in implementation
    scale: 'scale', // For scaling elements in or out, giving a sense of depth
    rotate: 'rotate', // For rotating elements, can be used for dynamic emphasis
    pulse: 'pulse', // For a pulsing effect, useful for drawing attention to interactive elements
    blink: 'blink', // For a blinking effect, subtle attention-getter without movement
    // Expanding types to cover more interactive and dynamic UI effects
    pathDraw: 'path-draw', // For SVG path animations, creating a drawing effect
    backgroundShift: 'background-shift', // For shifting background colors or images, adding a dynamic background effect
  },
  // This structure allows for expansion as the design system evolves
};

export default animations;
