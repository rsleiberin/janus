const shadow = {
  subtle: '0 1px 2px rgba(0, 0, 0, 0.18)', // Slightly softer than 'low', for subtle emphasis
  default: '0 2px 4px rgba(0, 0, 0, 0.24)', // Standard shadow for general use, replacing 'medium'
  emphasis: '0 4px 8px rgba(0, 0, 0, 0.32)', // More pronounced, for elements requiring emphasis, replaces 'high'
  ambient: '0 8px 16px rgba(0, 0, 0, 0.36)', // Larger, softer shadow for ambient effects, broader than 'emphasis'
  focus: '0 0 0 3px rgba(50, 50, 93, 0.4)', // For focus states, outlines, or floating elements
  inset: 'inset 0 2px 4px rgba(0, 0, 0, 0.06)', // Soft inner shadow for inset effects, making elements look embedded
};
