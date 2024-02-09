import React from 'react';
import styles from './imageStyles.module.css'; // Correctly import the new CSS module

const Image = ({ src, alt, className = '', onClick }) => {
  return (
    <img 
      src={src} 
      alt={alt} 
      className={`${styles.customImage} ${className}`} // Use styles from the module, and allow additional className props
      onClick={onClick} 
      loading="lazy" // Enables lazy loading for images
    />
  );
};

export default Image;
