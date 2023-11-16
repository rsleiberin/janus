import React from 'react';
import colors from '../design-tokens/colors';
import spacing from '../design-tokens/spacing';
import typography from '../design-tokens/typography';

const ProjectShowcase = ({ title, description }) => {
  // Update this line to use the path of your image
  const imageUrl = '/images/66.png'; 

  return (
    <div style={{
      border: `1px solid ${colors.gray[700]}`, // using color token for border
      padding: spacing.md, // using spacing token for padding
      borderRadius: '8px', // example radius, adjust as needed
      fontFamily: typography.fonts.body, // using typography token
    }}>
      {imageUrl && (
        <img
          src={imageUrl}
          alt={title}
          style={{
            width: '100%',
            height: 'auto',
            marginBottom: spacing.sm,
          }}
        />
      )}
      <h3 style={{
        fontSize: typography.fontSizes.lg,
        color: colors.white, // using color token for text
        marginBottom: spacing.sm,
      }}>
        {title}
      </h3>
      <p>{description}</p>
    </div>
  );
};

export default ProjectShowcase;
