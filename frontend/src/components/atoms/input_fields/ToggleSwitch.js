import React from 'react';
import styles from './toggleSwitchStyles.module.css'; // Corrected import path to CSS module

const ToggleSwitch = ({ checked, onChange, name, label }) => {
    return (
        <div className={styles['toggle-switch-container']}>
            {label && <label htmlFor={`toggle-${name}`} className={styles.label}>{label}</label>}
            <div className={styles['toggle-switch']}>
                <input
                    id={`toggle-${name}`}
                    className={styles['toggle-input']}
                    type="checkbox"
                    checked={checked}
                    onChange={onChange}
                    name={name}
                />
                <span className={styles.slider}></span>
            </div>
        </div>
    );
};

export default ToggleSwitch;
