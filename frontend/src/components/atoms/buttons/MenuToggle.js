import React, { useState } from 'react';
import styles from './menuToggleStyles.module.css'; // Corrected import path

// Menu Toggle Button Component
const MenuToggleButton = ({ icon, ariaLabel, onToggle }) => {
  const [isActive, setIsActive] = useState(false);

  const handleToggle = () => {
    setIsActive(!isActive);
    if (onToggle) {
      onToggle(!isActive);
    }
  };

  return (
    <button
      className={`${styles['menu-toggle-button']} ${isActive ? styles.active : ''}`}
      aria-label={ariaLabel}
      onClick={handleToggle}
    >
      {icon}
    </button>
  );
};

export default MenuToggleButton;
