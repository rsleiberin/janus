import React from 'react';
import Image from 'next/image';
import styles from './imageStyles.module.css';

const CustomImage = ({ src, alt, className = '', onClick }) => {
  return (
    <Image
      src={src}
      alt={alt}
      className={`${styles.customImage} ${className}`}
      onClick={onClick}
      width={500}
      height={500}
      loading="lazy"
    />
  );
};

export default CustomImage;