import React from 'react';
import './headingStyles.css';

const Heading = ({ level, text, className }) => {
  const Tag = `h${level}`;
  return <Tag className={`heading ${className}`}>{text}</Tag>;
};

export default Heading;
