import React from 'react';
import styles from './radioButtonStyles.module.css'; // Corrected import path to CSS module

const RadioButton = ({ label, checked, onChange, name, value }) => {
    return (
        <div className={styles['radio-button-container']}>
            <input
                id={`radio-${value}`}
                className={styles['radio-input']}
                type="radio"
                checked={checked}
                onChange={onChange}
                name={name}
                value={value}
            />
            <label htmlFor={`radio-${value}`} className={styles['radio-label']}>
                {label}
            </label>
        </div>
    );
};

export default RadioButton;
