import React, { useState } from 'react';
import MenuItem from './MenuItem';
import Icon from '../../atoms/content_and_media_elements/Icon';
import './dropdownMenuStyles.module.css';

// DropdownMenu Component
const DropdownMenu = ({ items }) => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleDropdown = () => setIsOpen(!isOpen);

    return (
        <div className="dropdown-menu-container">
            <button className="dropdown-toggle" onClick={toggleDropdown}>
                Menu <Icon icon={'▼'} ariaLabel="Toggle dropdown" />
            </button>
            {isOpen && (
                <ul className="dropdown-menu">
                    {items.map((item, index) => (
                        <MenuItem key={index} {...item} />
                    ))}
                </ul>
            )}
        </div>
    );
};

export default DropdownMenu;
