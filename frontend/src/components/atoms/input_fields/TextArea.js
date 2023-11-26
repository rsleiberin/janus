import React from 'react';
import './textAreaStyles.css'; // Link to your CSS file for TextArea

// TextArea Component
const TextArea = ({ placeholder, onChange, maxLength }) => {
    return (
        <textarea
            className="text-area"
            placeholder={placeholder}
            onChange={onChange}
            maxLength={maxLength}
        />
    );
};

export default TextArea;

// Notes:
// - This TextArea component allows for multi-line text input.
// - The 'maxLength' prop can be used to limit the character count.
// - Customization options include 'placeholder' text and 'onChange' handler.
// - It incorporates design tokens for typography, spacing, and color for consistent styling.
// - The component is resizable vertically, as per the responsive design best practices.
// - Style customization can be done via the linked 'textAreaStyles.css'.
