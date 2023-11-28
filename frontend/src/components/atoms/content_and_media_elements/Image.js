import React from 'react';
import './imageStyles.css'; // Link to your CSS file for Images

// Image Component
const Image = ({ src, alt, className, onClick }) => {
  return (
    <img 
      src={src} 
      alt={alt} 
      className={`custom-image ${className}`} 
      onClick={onClick} 
      loading="lazy" // Enables lazy loading for performance
    />
  );
};

export default Image;

// Notes:
// - The 'alt' attribute is essential for accessibility and SEO.
// - Use 'loading="lazy"' for lazy loading of off-screen images.
// - Customize the image's appearance and behavior using CSS and the 'className' prop.
