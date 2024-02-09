import React from 'react';
import styles from './floatingActionButtonStyles.module.css'; // Corrected import path

// FloatingActionButton Component
const FloatingActionButton = ({ icon, onClick, ariaLabel }) => {
  return (
    <button className={styles.fab} onClick={onClick} aria-label={ariaLabel}>
      {icon} {/* Icon should be an SVG or similar component */}
    </button>
  );
};

export default FloatingActionButton;
