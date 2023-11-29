import React from 'react';
import './gridLayoutStyles.css'; // Link to GridLayout CSS

const GridLayout = ({ children }) => {
  return (
    <div className="grid-layout">
      {children}
    </div>
  );
};

export default GridLayout;

// Notes:
// - The GridLayout component is designed to be flexible and responsive.
// - It automatically adjusts the number of columns based on screen size.
// - Customize the grid by editing the GridLayout.css file.
// - Utilize design tokens for consistent spacing and breakpoints.
