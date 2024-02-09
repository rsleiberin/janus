import React from 'react';
import styles from './textAreaStyles.module.css'; // Corrected import path to CSS module

const TextArea = ({ placeholder, onChange, maxLength }) => {
    return (
        <textarea
            className={styles['text-area']}
            placeholder={placeholder}
            onChange={onChange}
            maxLength={maxLength}
        />
    );
};

export default TextArea;
