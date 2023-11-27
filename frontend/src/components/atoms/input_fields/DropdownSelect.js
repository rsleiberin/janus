import React from 'react';
import './dropdownSelectStyles.css'; // Link to your CSS file for DropdownSelect

// DropdownSelect Component
const DropdownSelect = ({ label, options, onChange, value, name }) => {
    return (
        <div className="dropdown-select-container">
            {label && <label htmlFor={`dropdown-select-${name}`}>{label}</label>}
            <select
                id={`dropdown-select-${name}`}
                className="dropdown-select"
                onChange={onChange}
                value={value}
                name={name}
            >
                {options.map((option, index) => (
                    <option key={index} value={option.value}>
                        {option.label}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default DropdownSelect;

// Notes:
// - The component provides a dropdown for selecting a single option from a list.
// - It supports a label, which can be omitted if not needed.
// - Options are passed as an array of objects with 'label' and 'value' properties.
// - Customization options include 'onChange', 'value', and 'name' props.
// - The dropdown uses design tokens for consistent styling with the application.
// - Accessibility and responsive design are considered in its implementation.
