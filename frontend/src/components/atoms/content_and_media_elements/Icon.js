import React from 'react';
import styles from './iconStyles.module.css'; // Correctly import the CSS module

const Icon = ({ icon, ariaLabel, size = 'medium' }) => {
  return (
    <span 
      className={`${styles.icon} ${styles[`icon-${size}`]}`}
      aria-label={ariaLabel}
      style={{ fill: 'var(--color-text-primary)', stroke: 'var(--color-text-primary)' }} // Use CSS variables for colors
    >
      {icon} {/* Ensure icon is an SVG or similar component that can inherit color and size from CSS */}
    </span>
  );
};

export default Icon;
