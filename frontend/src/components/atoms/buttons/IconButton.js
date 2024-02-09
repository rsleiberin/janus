import React from 'react';
import styles from './iconButtonStyles.module.css'; // Corrected import path

// IconButton Component
const IconButton = ({ icon, onClick, ariaLabel, size = 'medium', styleType = 'primary' }) => {
  const className = `${styles['icon-btn']} ${styles[size]} ${styles[styleType]}`;

  return (
    <button className={className} onClick={onClick} aria-label={ariaLabel}>
      {icon} {/* Icon should be an SVG or similar component */}
    </button>
  );
};

export default IconButton;
