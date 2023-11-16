// Import necessary dependencies from Next.js and React
import Link from 'next/link';
import { useRouter } from 'next/router';
import React from 'react';
// Import your design tokens
import colors from '../design-tokens/colors';
import typography from '../design-tokens/typography';

const Navigation = () => {
  const router = useRouter();

  return (
    <nav style={{
      backgroundColor: colors.black, // using color token
      color: colors.white, // using color token
      fontFamily: typography.fonts.heading, // using typography token
      padding: '1rem 2rem', // example padding, replace with spacing token if you have
    }}>
      <div style={{ fontWeight: typography.fontWeights.bold }}>
        <Link href="/">
          <a style={{ color: colors.white, textDecoration: 'none' }}>LODESTONE</a>
        </Link>
      </div>
      <div>
        <Link href="/design">
          <a style={{
            color: router.pathname === "/design" ? colors.primary : colors.white,
            marginRight: '20px', // example margin, replace with spacing token if you have
          }}>Design</a>
        </Link>
        <Link href="/art">
          <a style={{
            color: router.pathname === "/art" ? colors.primary : colors.white,
            marginRight: '20px', // example margin, replace with spacing token if you have
          }}>Art</a>
        </Link>
        <Link href="/philosophy">
          <a style={{
            color: router.pathname === "/philosophy" ? colors.primary : colors.white,
          }}>Philosophy</a>
        </Link>
      </div>
    </nav>
  );
};

export default Navigation;
