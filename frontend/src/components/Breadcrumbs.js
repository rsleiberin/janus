// Import necessary dependencies from Next.js and React
import { useRouter } from 'next/router';
import React from 'react';
// Import your design tokens
import typography from '../design-tokens/typography';
import spacing from '../design-tokens/spacing';

const Breadcrumbs = () => {
  const router = useRouter();
  const path = router.pathname.split('/').filter(x => x);

  return (
    <div style={{
      fontFamily: typography.fonts.body, // using typography token
      padding: spacing.md, // using spacing token
    }}>
      <ul style={{ listStyle: 'none', display: 'flex' }}>
        <li style={{ marginRight: spacing.sm }}>
          <a href="/" style={{ textDecoration: 'none', color: 'inherit' }}>
            Home
          </a>
        </li>
        {path.map((segment, index) => (
          <li key={index} style={{ marginRight: spacing.sm }}>
            <a href={`/${segment}`} style={{ textDecoration: 'none', color: 'inherit' }}>
              {segment.charAt(0).toUpperCase() + segment.slice(1)}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Breadcrumbs;
