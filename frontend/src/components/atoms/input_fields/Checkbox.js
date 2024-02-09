import React from 'react';
import styles from './checkboxStyles.module.css'; // Corrected import path to CSS module

// Checkbox Component
const Checkbox = ({ label, checked, onChange, name }) => {
    return (
        <div className={styles['checkbox-container']}>
            <input
                id={`checkbox-${name}`}
                className={styles['checkbox-input']}
                type="checkbox"
                checked={checked}
                onChange={onChange}
                name={name}
            />
            <label htmlFor={`checkbox-${name}`} className={styles['checkbox-label']}>
                {label}
            </label>
        </div>
    );
};

export default Checkbox;
