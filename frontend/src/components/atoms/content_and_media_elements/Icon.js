import React from 'react';
import './iconStyles.css'; // Link to your CSS file for Icons

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
