import React from 'react';
import colors from '../design_tokens/colors';
import Header from '../organisms/Header'; // Assuming you have a Header component
import Footer from '../organisms/Footer'; // Assuming you have a Footer component
// Import other necessary components or design tokens

const MainLayout = ({ children }) => {
    return (
        <div style={{ backgroundColor: colors.lightBase, color: colors.textDark }}>
            <Header />
            <main>
                {children}
            </main>
            <Footer />
        </div>
    );
};

export default MainLayout;
