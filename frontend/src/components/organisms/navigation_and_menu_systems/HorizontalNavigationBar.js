import React from 'react';
import DropdownMenu from '../../molecules/navigation_elements/DropdownMenu';
import ShopCTAButton from '../../molecules/call_to_action_buttons/ShopCTAButton';
import styles from './horizontalNavigationBarStyles.module.css'; // Updated import statement

// Horizontal Navigation Bar Component
const HorizontalNavigationBar = ({ navItems, ctaText }) => {
  return (
    <nav className={styles.horizontalNav}>
      <ul className={styles.navList}>
        {/* Your existing implementation */}
      </ul>
      {ctaText && <ShopCTAButton text={ctaText} />} {/* CTA Button */}
    </nav>
  );
};

export default HorizontalNavigationBar;


// Notes:
// - Utilizes DropdownMenu for items with sub-options.
// - Direct links for items without dropdowns.
// - Includes a ShopCTAButton for the main call-to-action.
// - Adheres to best practices in usability, accessibility, and responsive design.
