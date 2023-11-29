import React from 'react';
import './listItemStyles.css'; // Link to the CSS file for ListItem

const ListItem = ({ primaryText, secondaryText, icon, onClick }) => {
  return (
    <div className="list-item" onClick={onClick}>
      {icon && <span className="icon">{icon}</span>}
      <div className="text-content">
        <p className="primary-text">{primaryText}</p>
        {secondaryText && <p className="secondary-text">{secondaryText}</p>}
      </div>
    </div>
  );
};

export default ListItem;

// Notes:
// - Use this component for creating list items with primary and secondary text.
// - Include an icon for visual emphasis and interaction.
// - Apply onClick for handling user interaction.
// - Customize by adding more props as needed for different use cases.
