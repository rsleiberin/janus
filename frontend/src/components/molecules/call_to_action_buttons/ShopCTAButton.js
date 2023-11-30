// ShopCTAButton.js
import React from 'react';
import './shopCTAButtonStyles.css'; // Link to your CSS file for this button

// Shop CTA Button Component
const ShopCTAButton = ({ text }) => {
  return (
    <button className="shop-cta-button">
      {text}
    </button>
  );
};

export default ShopCTAButton;

// Notes:
// - This component renders a button specific for the shop CTA.
// - The text for the button is passed as a prop.
