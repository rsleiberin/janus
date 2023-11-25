import React from 'react';
import './iconButtonStyles.css'; // Link to your CSS file for IconButtons

// IconButton Component
const IconButton = ({ icon, onClick, ariaLabel, size = 'medium', styleType = 'primary' }) => {
  const className = `icon-btn ${size} ${styleType}`;

  return (
    <button className={className} onClick={onClick} aria-label={ariaLabel}>
      {icon} {/* Icon should be an SVG or similar component */}
    </button>
  );
};

export default IconButton;

// Notes:
// - Ensure icons are SVGs for scalability and accessibility.
// - Utilize aria-label for screen reader accessibility.
// - CSS classes allow for customization of size and style.
