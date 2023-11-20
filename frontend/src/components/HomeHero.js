import React from 'react';
import Button from './Button'; // Assuming you have a Button component
import typography from '../design-tokens/typography';
import colors from '../design-tokens/colors';
import spacing from '../design-tokens/spacing';

const HomeHero = ({ title, description, buttonText }) => {
  return (
    <section style={{
      padding: spacing.lg,
      backgroundColor: colors.gray[900], // using color token for background
      color: colors.white, // using color token for text
    }}>
      <h1 style={{
        fontFamily: typography.fonts.heading,
        fontSize: typography.fontSizes.xl,
        marginBottom: spacing.md,
      }}>
        {title}
      </h1>
      <p style={{
        fontFamily: typography.fonts.body,
        fontSize: typography.fontSizes.base,
        marginBottom: spacing.md,
      }}>
        {description}
      </p>
      <Button text={buttonText} /> {/* Replace with your button component and styles */}
    </section>
  );
};

export default HomeHero;
