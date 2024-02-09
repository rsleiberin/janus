import React from 'react';
import styles from './listItemStyles.module.css'; // Corrected import path to CSS module

const ListItem = ({ primaryText, secondaryText, icon, onClick }) => {
  return (
    <div className={styles['list-item']} onClick={onClick}>
      {icon && <span className={styles.icon}>{icon}</span>}
      <div className={styles['text-content']}>
        <p className={styles['primary-text']}>{primaryText}</p>
        {secondaryText && <p className={styles['secondary-text']}>{secondaryText}</p>}
      </div>
    </div>
  );
};

export default ListItem;
