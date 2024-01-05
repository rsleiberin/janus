import React from 'react';
import colors from '../../../utilities/design_tokens/colors';
import responsive from '../../../utilities/design_tokens/responsive';
import styles from './iconStyles.module.css';

// Icon Component
const Icon = ({ icon, ariaLabel, size = 'medium' }) => {
  // Use the appropriate size from design tokens
  const sizeStyle = {
    small: {
      width: responsive.sizes.small,
      height: responsive.sizes.small
    },
    medium: {
      width: responsive.sizes.medium,
      height: responsive.sizes.medium
    },
    large: {
      width: responsive.sizes.large,
      height: responsive.sizes.large
    }
  };

  return (
    <span 
      className={styles.icon} 
      style={{ ...sizeStyle[size], fill: colors.primary, stroke: colors.primary }} 
      aria-label={ariaLabel}
    >
      {icon} {/* Icon should be an SVG or similar component */}
    </span>
  );
};

export default Icon;

// Notes:
// - Use SVG icons for scalability and accessibility.
// - The 'aria-label' attribute is essential for screen reader accessibility.
// - Icon size can be customized using the 'size' prop (small, medium, large).
