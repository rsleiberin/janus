import React from 'react';
import colors from '../design_tokens/colors';

const HomePage = () => {
    return (
        <div style={{ backgroundColor: colors.lightBase, color: colors.textDark }}>
            <header>
                {/* Header content goes here */}
                <h1>Welcome to Our Website</h1>
            </header>
            <main>
                {/* Main content goes here */}
                <p>This is the home page of our awesome application.</p>
            </main>
            <footer>
                {/* Footer content goes here */}
                <p>© 2023 Your Company Name</p>
            </footer>
        </div>
    );
};

export default HomePage;
