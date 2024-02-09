import React, { useState } from 'react';
import MenuItem from './MenuItem'; // Adjust the import path as needed
import Icon from '../../atoms/content_and_media_elements/Icon'; // Verify the import path
import styles from './dropdownMenuStyles.module.css'; // Correct path to CSS module

// DropdownMenu Component
const DropdownMenu = ({ items }) => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleDropdown = () => setIsOpen(!isOpen);

    return (
        <div className={styles.dropdownMenuContainer}>
            <button className={styles.dropdownToggle} onClick={toggleDropdown}>
                Menu <Icon icon={'▼'} ariaLabel="Toggle dropdown" />
            </button>
            {isOpen && (
                <ul className={styles.dropdownMenu}>
                    {items.map((item, index) => (
                        <MenuItem key={index} {...item} />
                    ))}
                </ul>
            )}
        </div>
    );
};

export default DropdownMenu;
