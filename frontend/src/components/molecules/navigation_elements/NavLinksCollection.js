// NavLinksCollection.js
import React from 'react';
import NavLink from '../atoms/navigation_elements/NavLink';
import styles from './navLinksCollectionStyles.module.css'; // Make sure to create this CSS module file

const NavLinksCollection = ({ links }) => {
  return (
    <ul className={styles.navList}>
      {links.map((link, index) => (
        <NavLink key={index} href={link.href} label={link.label} />
      ))}
    </ul>
  );
};

export default NavLinksCollection;
