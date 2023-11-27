import React from 'react';
import './textFieldStyles.css'; // Link to your CSS file for TextFields

// TextField Component
const TextField = ({ type = 'text', placeholder, onChange, value, name }) => {
  return (
    <input
      className="text-field"
      type={type}
      placeholder={placeholder}
      onChange={onChange}
      value={value}
      name={name}
    />
  );
};

export default TextField;

// Notes:
// - The component is designed to be versatile, handling various text input types.
// - It uses design tokens for consistent styling with the rest of the application.
