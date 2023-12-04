import React from 'react';
import DropdownMenu from './DropdownMenu';
import ShopCTAButton from './ShopCTAButton';
import './horizontalNavigationBarStyles.css'; // Ensure to link to your CSS file for the horizontal navigation bar

// Horizontal Navigation Bar Component
const HorizontalNavigationBar = ({ navItems, ctaText }) => {
  return (
    <nav className="horizontal-nav">
      <ul className="nav-list">
        {navItems.map((item, index) => (
          // Render DropdownMenu or simple link based on item type
          item.dropdownItems ? (
            <li key={index}><DropdownMenu items={item.dropdownItems} /></li>
          ) : (
            <li key={index}><a href={item.link}>{item.label}</a></li>
          )
        ))}
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
