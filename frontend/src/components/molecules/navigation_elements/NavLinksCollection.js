// NavLinksCollection.js
import React from 'react';
import NavLink from '../../atoms/navigation_elements/NavLink';
import styles from './navLinksCollectionStyles.module.css';

const NavLinksCollection = ({ links }) => {
  return (
    <ul className={styles.navList}>
      {links.map((link, index) => (
        <NavLink key={index} {...link} />
      ))}
    </ul>
  );
};

export default NavLinksCollection;
