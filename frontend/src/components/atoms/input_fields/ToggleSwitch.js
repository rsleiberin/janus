import React from 'react';
import './toggleSwitchStyles.css'; // Link to your CSS file for ToggleSwitch

// ToggleSwitch Component
const ToggleSwitch = ({ checked, onChange, name, label }) => {
    return (
        <div className="toggle-switch-container">
            {label && <label htmlFor={`toggle-${name}`}>{label}</label>}
            <div className="toggle-switch">
                <input
                    id={`toggle-${name}`}
                    className="toggle-input"
                    type="checkbox"
                    checked={checked}
                    onChange={onChange}
                    name={name}
                />
                <span className="slider"></span>
            </div>
        </div>
    );
};

export default ToggleSwitch;

// Notes:
// - The component functions as a switch between two states, typically 'on' and 'off'.
// - It utilizes design tokens for consistent and responsive styling.
// - Customization options include 'checked', 'onChange', 'name', and optional 'label' props.
// - Visual feedback is provided for interaction states.
