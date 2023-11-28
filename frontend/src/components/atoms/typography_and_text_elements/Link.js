import React from 'react';
import './LinkStyles.css';

// Link component for achromatic, image-driven design.
// 'href' for URL and 'text' for display text.
const Link = ({ href, text }) => {
  return <a href={href} className="achromatic-link">{text}</a>;
};

export default Link;

// Usage:
// <Link href="https://example.com" text="Visit Example" />
