import React from 'react';
import Link from 'next/link';
import styles from './navLinkStyles.module.css';

const NavLink = ({ href, label, active }) => {
  const activeStyle = {
    design: styles.activeDesign,
    art: styles.activeArt,
    philosophy: styles.activePhilosophy,
  }[href.slice(1)]; // Extract the path without the leading slash and use it to determine the active style

  return (
    <li className={styles.navItem}>
      {/* Updated Link usage without <a> tag */}
      <Link href={href} className={`${styles.navLink} ${active ? activeStyle : ''}`}>
        {label}
      </Link>
    </li>
  );
};

export default NavLink;
