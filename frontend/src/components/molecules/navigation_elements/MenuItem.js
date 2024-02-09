import React from 'react';
import styles from './menuItemStyles.module.css'; // Correctly import the CSS module

// MenuItem Component
const MenuItem = ({ label, link, icon, onClick }) => {
    return (
        <li className={styles.menuItem}>
            {icon && <span className={styles.menuItemIcon}>{icon}</span>}
            <a href={link} onClick={onClick} className={styles.menuItemLink}>
                {label}
            </a>
        </li>
    );
};

export default MenuItem;
