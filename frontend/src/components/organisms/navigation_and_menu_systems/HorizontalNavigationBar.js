import React from 'react';
import Link from 'next/link'; // Import Link for routing
import ShopCTAButton from '../../molecules/call_to_action_buttons/ShopCTAButton';
import LogoPlaceholder from '../../atoms/navigation_elements/LogoPlaceholder'; // Updated import path
import styles from './horizontalNavigationBarStyles.module.css'; // Corrected import statement

// Horizontal Navigation Bar Component
const HorizontalNavigationBar = ({ navItems, ctaText }) => {
  return (
    <nav className={styles.horizontalNav}>
      <Link href="/" passHref>
        <a><LogoPlaceholder /></a> {/* Logo acting as a home button */}
      </Link>
      <ul className={styles.navList}>
        {/* Iterate over navItems to render each as either a DropdownMenu or a direct link */}
        {/* Placeholder for nav items */}
      </ul>
      {ctaText && <ShopCTAButton text={ctaText} />} {/* CTA Button utilizing global design tokens */}
    </nav>
  );
};

export default HorizontalNavigationBar;
