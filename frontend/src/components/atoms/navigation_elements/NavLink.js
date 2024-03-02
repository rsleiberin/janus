// NavLink.js
import React from 'react';
import Link from 'next/link';
import styles from './navLinkStyles.module.css'; // Make sure to create this CSS module file

const NavLink = ({ href, label }) => {
  return (
    <li className={styles.navItem}>
      <Link href={href}>
        <a className={styles.navLink}>{label}</a>
      </Link>
    </li>
  );
};

export default NavLink;
