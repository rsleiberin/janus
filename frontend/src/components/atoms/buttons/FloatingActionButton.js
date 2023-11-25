import React from 'react';
import './floatingActionButtonStyles.css'; // Link to your CSS file for FABs

// FloatingActionButton Component
const FloatingActionButton = ({ icon, onClick, ariaLabel }) => {
  return (
    <button className="fab" onClick={onClick} aria-label={ariaLabel}>
      {icon} {/* Icon should be an SVG or similar component */}
    </button>
  );
};

export default FloatingActionButton;

// Notes:
// - Use SVG icons for better accessibility and scalability.
// - Ensure aria-label is used for screen reader accessibility.
// - The button size and position can be adjusted using CSS.
