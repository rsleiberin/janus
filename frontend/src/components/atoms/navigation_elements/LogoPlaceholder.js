import React from 'react';
import Link from 'next/link';
import styles from './logoPlaceholderStyles.module.css';

const LogoPlaceholder = () => {
    return (
        <Link href="/" passHref>
            <div className={styles.logoPlaceholder}></div>
        </Link>
    );
};

export default LogoPlaceholder;
