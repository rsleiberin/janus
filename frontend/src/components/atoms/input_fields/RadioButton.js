import React from 'react';
import './radioButtonStyles.css'; // Link to your CSS file for RadioButton

// RadioButton Component
const RadioButton = ({ label, checked, onChange, name, value }) => {
    return (
        <div className="radio-button-container">
            <input
                id={`radio-${value}`}
                className="radio-input"
                type="radio"
                checked={checked}
                onChange={onChange}
                name={name}
                value={value}
            />
            <label htmlFor={`radio-${value}`} className="radio-label">
                {label}
            </label>
        </div>
    );
};

export default RadioButton;

// Notes:
// - The component allows selection of a single option within a group.
// - It uses design tokens for consistent styling.
// - Customization options include 'label', 'checked', 'onChange', 'name', and 'value' props.
// - The radio button provides visual feedback for different states.
