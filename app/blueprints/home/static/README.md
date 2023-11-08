# Static Directory - Janus Home Blueprint

## Introduction
This `static` directory is a central hub for all static assets used in the `home` blueprint of the Janus Flask application. Assets include stylesheets, JavaScript files, and images which enhance the aesthetics and functionality of the home page.

## Directory Structure and Contents
- `css`: Stores the Tailwind CSS stylesheet files and any additional custom CSS needed for the `home` section. Currently contains an empty `app.css` which will hold custom styles.
- `img`: Dedicated to housing images, icons, and other visual media for the `home` blueprint. Presently, this directory is empty and will be populated with relevant assets as they are created.
- `js`: Contains JavaScript files responsible for adding interactivity and improved user experience. Contains an empty `main.js` file which will include the necessary scripts.

## Usage Guidelines
- All static resources should be optimized for efficiency to ensure fast page load times.
- The generated Tailwind CSS file should include only the necessary utilities, leveraging PurgeCSS to remove unused styles.
- Versioning and caching strategies should be applied to the static assets to enhance client-side performance.
- Regular audits and updates of static files are recommended to maintain optimal performance and incorporate new features.

## Notes
- As the project evolves, this centralized documentation will be updated to reflect any changes to the file structure or asset strategy.
- Where necessary, more detailed documentation may be provided within specific files, such as CSS or JavaScript, where inline comments can explain the purpose and use of particular styles or scripts.