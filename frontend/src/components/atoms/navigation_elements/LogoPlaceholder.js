// LogoPlaceholder.js
import React from 'react';
import Link from 'next/link';
import styles from './logoPlaceholderStyles.module.css'; // CSS Module for styling

const LogoPlaceholder = ({ logoSrc }) => {
  return (
    <Link href="/">
      <a className={styles.logoContainer}>
        {logoSrc ? (
          <img src={logoSrc} alt="Logo" className={styles.logo} />
        ) : (
          <div className={styles.placeholder}></div>
        )}
      </a>
    </Link>
  );
};

export default LogoPlaceholder;
