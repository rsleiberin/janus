import React from 'react';
import './checkboxStyles.css'; // Link to your CSS file for Checkbox

// Checkbox Component
const Checkbox = ({ label, checked, onChange, name }) => {
    return (
        <div className="checkbox-container">
            <input
                id={`checkbox-${name}`}
                className="checkbox-input"
                type="checkbox"
                checked={checked}
                onChange={onChange}
                name={name}
            />
            <label htmlFor={`checkbox-${name}`} className="checkbox-label">
                {label}
            </label>
        </div>
    );
};

export default Checkbox;

// Notes:
// - The component is designed for simple integration with forms and UI elements.
// - It uses design tokens for consistent styling.
// - Customization options include 'label', 'checked', 'onChange', and 'name' props.
// - The checkbox provides visual feedback and accessibility features.
