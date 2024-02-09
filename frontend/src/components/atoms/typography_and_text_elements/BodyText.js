import React from 'react';
import styles from './bodyTextStyles.module.css'; // Corrected import path to CSS module

const BodyText = ({ text, className = '' }) => {
  return <p className={`${styles['body-text']} ${className}`}>{text}</p>;
};

export default BodyText;
