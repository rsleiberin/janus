// Import your design tokens directly into your component file
import React from 'react';
import colors from '../../../utilities/design_tokens/colors';
import icons from '../../../utilities/design_tokens/icons'; // Assuming this file exists and has size tokens
import styles from './iconStyles.module.css';

const Icon = ({ icon, ariaLabel, size = 'medium' }) => {
  // Dynamically set the icon size using design tokens
  const sizeStyles = {
    small: {
      width: icons.sizes.small,  // Assuming 'sizes' and 'small' are valid keys in your icons design tokens
      height: icons.sizes.small,
    },
    medium: {
      width: icons.sizes.medium,
      height: icons.sizes.medium,
    },
    large: {
      width: icons.sizes.large,
      height: icons.sizes.large,
    },
  };

  return (
    <span 
      className={`${styles.icon} ${styles[`icon${size.charAt(0).toUpperCase() + size.slice(1)}`]}`}
      style={{ ...sizeStyles[size], fill: colors.black, stroke: colors.black }}
      aria-label={ariaLabel}
    >
      {icon} {/* Icon should be an SVG or similar component */}
    </span>
  );
};

export default Icon;
