import React from 'react';
import ShopCTAButton from '../../molecules/call_to_action_buttons/ShopCTAButton';
import styles from './horizontalNavigationBarStyles.module.css'; // Corrected import statement

// Horizontal Navigation Bar Component
const HorizontalNavigationBar = ({ navItems, ctaText }) => {
  return (
    <nav className={styles.horizontalNav}>
      <ul className={styles.navList}>
        {/* Iterate over navItems to render each as either a DropdownMenu or a direct link */}
      </ul>
      {ctaText && <ShopCTAButton text={ctaText} />} {/* CTA Button utilizing global design tokens */}
    </nav>
  );
};

export default HorizontalNavigationBar;
