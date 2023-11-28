import React from 'react';
import './BodyTextStyles.css';

// BodyText component for rendering paragraph text.
// 'text' prop for the content and 'className' for additional styling.
const BodyText = ({ text, className }) => {
  return <p className={`body-text ${className}`}>{text}</p>;
};

export default BodyText;

// Usage:
// <BodyText text="Your text here" className="custom-style" />
