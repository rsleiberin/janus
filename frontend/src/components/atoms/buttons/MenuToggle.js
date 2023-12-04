import React, { useState } from 'react';
import './menuToggleButtonStyles.css'; // Link to the CSS file for the menu toggle button

// Menu Toggle Button Component
const MenuToggleButton = ({ icon, ariaLabel, onToggle }) => {
  const [isActive, setIsActive] = useState(false);

  // Toggles the active state of the button
  const handleToggle = () => {
    setIsActive(!isActive);
    if (onToggle) {
      onToggle(!isActive);
    }
  };

  return (
    <button
      className={`menu-toggle-button ${isActive ? 'active' : ''}`}
      aria-label={ariaLabel}
      onClick={handleToggle}
    >
      {icon}
    </button>
  );
};

export default MenuToggleButton;

// Notes:
// - This component toggles its active state on click and executes the onToggle callback.
// - The 'active' class is applied based on the button's state for styling purposes.
// - Include iconography and aria-label for accessibility and intuitive design.
// - Leverages design tokens for consistent styling and responsiveness.
