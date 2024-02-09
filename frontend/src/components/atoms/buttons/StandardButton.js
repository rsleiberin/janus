import React from 'react';
import styles from './standardButtonStyles.module.css'; // Corrected import path and switched to module.css

// Standard Button Component
const StandardButton = ({ text, size = 'medium', styleType = 'primary', onClick }) => {
  const className = `${styles.btn} ${styles[size]} ${styles[styleType]}`;

  return (
    <button className={className} onClick={onClick}>
      {text}
    </button>
  );
};

export default StandardButton;
