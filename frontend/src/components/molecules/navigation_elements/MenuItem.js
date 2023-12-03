import React from 'react';
import './menuItemStyles.css'; // Link to your CSS file for MenuItem

// MenuItem Component
const MenuItem = ({ label, link, icon, onClick }) => {
    return (
        <li className="menu-item">
            {icon && <span className="menu-item-icon">{icon}</span>}
            <a href={link} onClick={onClick} className="menu-item-link">
                {label}
            </a>
        </li>
    );
};

export default MenuItem;

// Notes:
// - 'MenuItem' represents a single item in a navigation menu.
// - It can include text, a link, an optional icon, and an onClick handler.
// - The component is designed to be flexible and easily customizable.
// - Use the 'label' prop for the menu item's text.
// - The 'link' prop is for the URL the menu item should navigate to.
// - The 'icon' prop can be used to pass an icon component (optional).
// - The 'onClick' prop allows for custom click event handling (optional).
// - This component should be used within a parent navigation list (`<ul>` or `<nav>`).
