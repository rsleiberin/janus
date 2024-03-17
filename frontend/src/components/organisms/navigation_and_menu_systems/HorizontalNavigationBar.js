// HorizontalNavigationBar.js
import React from 'react';
import ShopCTAButton from '../../molecules/call_to_action_buttons/ShopCTAButton';
import LogoPlaceholder from '../../atoms/navigation_elements/LogoPlaceholder';
import NavLinksCollection from '../../molecules/navigation_elements/NavLinksCollection';
import styles from './horizontalNavigationBarStyles.module.css';

const HorizontalNavigationBar = ({ currentPage }) => {
  const links = [
    { href: '/design', label: 'Design', active: currentPage === 'design' },
    { href: '/art', label: 'Art', active: currentPage === 'art' },
    { href: '/philosophy', label: 'Philosophy', active: currentPage === 'philosophy' },
  ];

  return (
    <nav className={styles.horizontalNav}>
      <LogoPlaceholder />
      <NavLinksCollection links={links} />
      <ShopCTAButton text="Shop" />
    </nav>
  );
};

export default HorizontalNavigationBar;
