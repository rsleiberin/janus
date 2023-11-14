# Project Structure Overview

## Major Components

- **Frontend**: The user interface of the application, developed using Next.js and styled with Tailwind CSS. Located in the `frontend/` directory.
- **Backend**: The server-side logic of the application, built with Flask. Located in the `app/` directory.
- **Design System**: A collection of design tokens, best practices, and visual assets that guide the UI/UX of the application. Located in the `documentation/design_system/` directory.

## Component Interactions

- The **Design System** defines the visual language and design guidelines which are implemented in the **Frontend** to ensure a consistent user experience.
- The **Frontend** serves the application's interface, which interacts with the **Backend** to process data and handle business logic.
- The **Backend** manages the server, application logic, databases, and serves data to the **Frontend** based on the defined routes and controllers.
