# Janus Frontend (Next.js)

This frontend is part of the overall **Janus** project, focused on accessible design and automated image analysis workflows. It leverages **Next.js** for a modern development experience and is currently deployed on Vercel.

---

## Overview

The Janus frontend showcases a component-driven approach, emphasizing **atomic design**, **reusable styles**, and **accessibility**. It is under active development to become both a personal portfolio site and a reusable engine for inclusive UI patterns.

---

## Getting Started

1. **Install Dependencies**  
   - Ensure Node.js is installed.  
   - In the frontend folder, run npm install (or yarn).

2. **Local Development**  
   - Run npm run dev to start the local dev server.  
   - Access the site at http://localhost:3000.

3. **Production Build**  
   - Run npm run build to create an optimized production bundle.  
   - Deploy via npm run start (or to your preferred hosting, like Vercel).

---

## Directory Structure

- **.gitignore / .eslintrc.json / next.config.js / tsconfig.json**  
  Core configuration files for Next.js, TypeScript declarations, ESLint rules, etc.

- **app/**  
  Currently empty; may be used if migrating to the Next.js App Router in the future.

- **public/**  
  Assets such as images (e.g., public/images/66.png) that Next.js can serve statically.

- **src/**  
  Houses all primary code. Key subfolders include:
  - **3D_components & animations/**  
    Early research notes or placeholders for advanced features.
  - **components/**  
    Follows an **Atomic Design** approach:
    - **atoms**: Basic building blocks (Button, Icon, InputField), each with a .module.css.
    - **molecules**: Compositions of atoms (e.g., DropdownMenu + MenuItem).
    - **organisms**: Larger, self-contained sections (e.g., HorizontalNavigationBar).
  - **contexts/**  
    (Empty or partially implemented) for React Context API usage.
  - **hooks/**  
    (Empty or partially implemented) custom React hooks could go here.
  - **layouts/**  
    Layout components that wrap pages (e.g., MainLayout.js with header/footer).
  - **pages/**  
    Standard Next.js page routing (index.js, art.js, etc.).  
    - _app.js: Global app configuration (e.g., global styles, providers).
  - **styles/**  
    Global styles (globals.css) that apply across the entire application.
  - **templates/**  
    Placeholder or advanced usage for page/component templates.
  - **tests/**  
    (If present) testing files or frameworks for frontend components.
  - **utilities/**  
    Shared logic or resources such as an axiosInstance.js or design_tokens/ for consistent styling.

- **node_modules/**, **.next/**  
  Automatically managed; contain dependencies and Next.js build artifacts.

---

## Accessibility & Design Focus

- **Atomic Design**  
  Each level (atoms, molecules, organisms) helps maintain clarity and reusability.
- **WCAG Alignment**  
  The eventual goal is to tie color palettes and text contrast to meet or exceed WCAG guidelines.  
  Future enhancements will integrate the backend’s image-analysis data to generate accessible color themes dynamically.

---

## Deployment

This project is deployed on Vercel. To deploy manually:
1. Push or import the frontend folder into a new Vercel project.
2. Use the default Next.js build settings.
3. Set up any environment variables (if needed for API calls or dynamic config).

---

## Best Practices

1. **Consistent Styling**  
   All CSS is modularized (*.module.css) to avoid naming collisions. Explore global design tokens in utilities/design_tokens/.
2. **Reusable Components**  
   Favor smaller, generic atoms that can scale into higher-level organisms.  
3. **Accessible Markup**  
   Where possible, include semantic HTML tags and ARIA attributes. For images, provide alt text.  
4. **Linting & Quality**  
   Use the existing ESLint config (.eslintrc.json) to keep code consistent.  
5. **Performance Optimizations**  
   Next.js supports image optimization (<Image />) and static exports. Watch for large media files and ensure lazy loading if feasible.

---

## Next Steps

- **Refine Content & Style**  
  Finalize the portfolio pages and ensure consistent branding/design token usage.
- **Enhance Testing**  
  Add or expand unit/integration tests under src/tests/ for critical components and pages.
- **Integrate Backend**  
  Hook up the APIs from backend for dynamic image analysis and data-driven theming.
- **Expand Atomic Library**  
  Flesh out unimplemented sections (molecules, organisms) and incorporate advanced interactions (3D, animations) gradually.

---

## Contributing

Open to feedback, suggestions, and contributions. Submit a pull request or open an issue if you find a bug or have an idea for improvement.

---

## License

This project is part of Janus, distributed under the [MIT License](../LICENSE).

---

_Thank you for exploring the Janus Frontend!_