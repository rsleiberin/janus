import React from 'react';
import './buttonStyles.css'; // Ensure to link to your CSS file for buttons

// Standard Button Component
const StandardButton = ({ text, size = 'medium', styleType = 'primary', onClick }) => {
  // className combines the size and styleType to fetch the right styles
  const className = `btn ${size} ${styleType}`;

  return (
    <button className={className} onClick={onClick}>
      {text}
    </button>
  );
};

export default StandardButton;

// Notes: 
// - This component uses CSS classes based on size and styleType for easy customization.
// - Add more `size` and `styleType` options in the CSS file for greater variety.
// - Ensure the CSS file uses variables from the design tokens for consistency.
