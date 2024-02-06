import React from 'react';
import DropdownItem from '../DropdownItem';
import styles from './megaDropdownMenu.module.css';

const MegaDropdownMenu = ({ categories }) => {
  return (
    <div className={styles.megaMenu}>
      {categories.map((category, index) => (
        <div key={index} className={styles.megaMenuCategory}>
          <h4 className={styles.megaMenuTitle}>{category.title}</h4>
          <ul className={styles.megaMenuList}>
            {category.items.map((item, itemIndex) => (
              <DropdownItem key={itemIndex} {...item} />
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default MegaDropdownMenu;
