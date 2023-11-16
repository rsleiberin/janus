import React from 'react';
import spacing from '../design-tokens/spacing';

const OrganismGrid = ({ children }) => {
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', // This creates a responsive grid
      gap: spacing.md, // using spacing token for grid gap
      padding: spacing.md, // using spacing token for padding
    }}>
      {children}
    </div>
  );
};

export default OrganismGrid;
