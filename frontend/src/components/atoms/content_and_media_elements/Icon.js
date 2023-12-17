import React from 'react';
import styles from './iconStyles.module.css'; // Updated to use the module

// Icon Component
const Icon = ({ icon, ariaLabel, size = 'medium' }) => {
  return (
    <span className={`icon icon-${size}`} aria-label={ariaLabel}>
      {icon} {/* Icon should be an SVG or similar component */}
    </span>
  );
};

export default Icon;

// Notes:
// - Use SVG icons for scalability and accessibility.
// - The 'aria-label' attribute is essential for screen reader accessibility.
// - Icon size can be customized using the 'size' prop (small, medium, large).
