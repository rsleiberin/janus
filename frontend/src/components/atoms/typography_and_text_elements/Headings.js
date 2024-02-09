import React from 'react';
import styles from './headingStyles.module.css'; // Corrected import path to CSS module

const Heading = ({ level, text, className = '' }) => {
  const Tag = `h${level}`;
  return <Tag className={`${styles.heading} ${styles[`heading-${level}`]} ${className}`}>{text}</Tag>;
};

export default Heading;
