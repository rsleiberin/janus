// ShopCTAButton.js
import React from 'react';
import styles from './shopCTAButtonStyles.module.css'; // Correct named import for CSS module

// Shop CTA Button Component
const ShopCTAButton = ({ text }) => {
  return (
    <button className={styles.shopCtaButton}> {/* Apply the styles object here */}
      {text}
    </button>
  );
};

export default ShopCTAButton;
