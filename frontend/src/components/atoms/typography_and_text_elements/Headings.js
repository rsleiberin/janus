import React from 'react';
import './HeadingStyles.css';

const Heading = ({ level, text, className }) => {
  const Tag = `h${level}`;
  return <Tag className={`heading ${className}`}>{text}</Tag>;
};

export default Heading;
