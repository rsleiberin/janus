import React from 'react';
import styles from './gridLayoutStyles.module.css'; // Corrected import path to CSS module

const GridLayout = ({ children }) => {
  return <div className={styles['grid-layout']}>{children}</div>;
};

export default GridLayout;
