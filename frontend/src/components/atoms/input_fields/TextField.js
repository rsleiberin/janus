import React from 'react';
import styles from './textFieldStyles.module.css'; // Corrected import path to CSS module

const TextField = ({ type = 'text', placeholder, onChange, value, name }) => {
  return (
    <input
      className={styles['text-field']}
      type={type}
      placeholder={placeholder}
      onChange={onChange}
      value={value}
      name={name}
    />
  );
};

export default TextField;
