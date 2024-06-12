import React from 'react';
import HorizontalNavigationBar from '../../components/organisms/navigation_and_menu_systems/HorizontalNavigationBar';
// Import any necessary design tokens or sub-components

const Header = () => {
    const navItems = [
        // Define navigation items here
    ];

    return (
        <header>
            <HorizontalNavigationBar navItems={navItems} ctaText="Shop" />
            {/* breadcrumb bar */}
        </header>
    );
};

export default Header;
