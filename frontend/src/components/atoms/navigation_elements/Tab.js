import React from 'react';
import './tabStyles.css'; // Link to your CSS file for Tabs

// Tab Component
const Tab = ({ label, activeTab, onClick, tabId }) => {
    return (
        <li className={`tab-item ${activeTab === tabId ? 'active' : ''}`} onClick={() => onClick(tabId)}>
            {label}
        </li>
    );
};

export default Tab;

// Notes:
// - The component represents an individual tab.
// - 'activeTab' determines if the tab is currently active.
// - 'onClick' handles tab switching and content rendering.
// - Customization options include the label and tabId.
// - The component uses design tokens for consistent styling.
