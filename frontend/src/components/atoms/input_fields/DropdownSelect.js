import React from 'react';
import styles from './dropdownSelectStyles.module.css'; // Corrected import path to CSS module

// DropdownSelect Component
const DropdownSelect = ({ label, options, onChange, value, name }) => {
    return (
        <div className={styles['dropdown-select-container']}>
            {label && <label htmlFor={`dropdown-select-${name}`} className={styles.label}>{label}</label>}
            <select
                id={`dropdown-select-${name}`}
                className={styles['dropdown-select']}
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
