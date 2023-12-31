import React from 'react';
import colors from '../utilities/design_tokens/colors';
import Header from '../components/organisms/Header'; // Assuming the Header component is in this path
import Footer from '../components/organisms/Footer'; // Assuming the Footer component is in this path

const HomePage = () => {
    return (
        <div style={{ backgroundColor: colors.lightBase, color: colors.textDark }}>
            <Header />
            <main>
                {/* Main content goes here */}
                <p>This is the home page of our awesome application.</p>
            </main>
            <Footer />
        </div>
    );
};

export default HomePage;
