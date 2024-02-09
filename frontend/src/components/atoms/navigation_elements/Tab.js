import React from 'react';
import styles from './tabStyles.module.css'; // Corrected import path to CSS module

const Tab = ({ label, activeTab, onClick, tabId }) => {
    return (
        <li className={`${styles['tab-item']} ${activeTab === tabId ? styles.active : ''}`} onClick={() => onClick(tabId)}>
            {label}
        </li>
    );
};

export default Tab;
