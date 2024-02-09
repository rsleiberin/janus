import React from 'react';
import styles from './linkStyles.module.css'; // Corrected import path to CSS module

const Link = ({ href, text }) => {
  return <a href={href} className={styles['achromatic-link']}>{text}</a>;
};

export default Link;
