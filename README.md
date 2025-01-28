# Janus

Janus is an **open-source** project that aims to streamline **accessible design** and automated workflows for **image analysis** in modern web applications. It provides a **Next.js** frontend and a **Flask (Python)** backend, enabling rapid experimentation in areas like **design systems**, **luminosity-based theming**, and **AI-driven insights** for usability. The project is intended as a **personal portfolio** to showcase growth and capabilities, while also inviting collaboration from the open-source community.

---

## Inspiration & Motivation

**Human-Centered Interaction**: With an M.S. in HCI, I’ve observed that many organizations fail to meet accessibility standards. Corporate design often overlooks how vital accessibility is, especially for inclusive user interfaces.

**COVID-Era Exploration**: After being laid off during the pandemic, I delved into AI (ChatGPT, Midjourney) to create large sets of branded or thematic images. I found that typical web design processes did not align well with my custom images or accessibility ideals, prompting me to build a **toolchain** that handles:
- **Dynamic image analysis** for color/luminosity data.
- **WCAG-aligned** theming and design tokens.
- Automated content adjustments to ensure clarity for diverse users.

**Personal Growth**: This repository shows my commitment to learning. I’m exploring advanced accessibility, color theory, and consistent design patterns, hoping to **demonstrate competency** to potential employers and the open-source community.

---

## High-Level Goals

1. **Adaptive UI Generation**  
   - Generate or extract color palettes and design tokens from images, reapplying them to web interfaces in an **accessible** manner.

2. **Human-Centered AI**  
   - Integrate AI agents to assist with everything from **image classification** to **design token refinement** based on **real-time** data, eventually exploring custom model integrations.

3. **Portfolio & Reference**  
   - Serve as a living example of code quality, with consistent linting (Flake8, Black, Pylint) and modular organization.  
   - Offer prospective employers and collaborators a clear window into my work ethic and approach.

4. **Future-Proofing**  
   - Migrate from SQLite to a production-capable database once the system’s storage/query requirements are well understood.  
   - Expand Next.js front-end for a robust, highly accessible portfolio.

---

## Current Status

- **Frontend (Next.js)**  
  - Basic routing is done; a custom CSS/tokens approach is under research.  
  - Not yet styled or populated with final content.  
  - Will deploy to Vercel under a custom domain as a **portfolio** front door.

- **Backend (Flask)**  
  - Fully linted and follows a layered architecture (routes, models, utils).  
  - Uses SQLite for development; planned upgrade to a more robust DB.  
  - Not thoroughly tested in its latest form; an older stable version is referenced in the repository history.

- **Image Processing**  
  - Work in progress; placeholders exist for scripts analyzing color, luminosity, and advanced clustering.  
  - Future plans include automatically extracting design tokens from images to inform UI theming.

- **Documentation**  
  - The `docs/` folder contains research notes and early concept documents:
    - **design_system**: Preliminary UX research and design token ideas.
    - **kami**: Experiments with custom GPT instructions, prototypes of AI workflow logic, and behind-the-scenes thinking on advanced agent protocols.
  - Other folders (e.g., `scripts/`, `integrations/`) showcase partial or early-stage code for data manipulation and possible external service integration.

- **Testing**  
  - A `tests/` directory contains initial Python tests for the backend.  
  - Test coverage is not complete, but a framework is in place for future expansions.

---

## Directory Overview

- **backend/**  
  Flask-based server logic, including models, routes, and utilities. Under active refactoring to ensure maintainable code quality.
  
- **frontend/**  
  Next.js application for the user-facing interface, eventually showcasing dynamic theming and custom design tokens extracted from user images.

- **docs/**  
  Contains research notes on design tokens, AI “kami” experiments, and general project architecture. Reflects the project’s rapid evolution and experimental approach.

- **image_processing/**  
  Scripts and data folders for analyzing images (color, luminosity, clustering). Plans to integrate deeper with the Flask backend for dynamic theming and data storage.

- **integrations/**  
  Currently empty; intended for future modules or scripts that connect Janus to other services (APIs, OAuth, third-party libraries).

- **scripts/**  
  Proof-of-concept or research scripts (e.g., relative luminance charts, color distribution). Helps guide the front- and back-end design decisions.

- **tests/**  
  Houses test suites for the Flask backend and any future code modules. Organized similarly to the backend’s folder structure for easy coverage.

- **uploads/**  
  Sample images for demonstration or testing. May be moved or reorganized pending final architecture decisions.

---

## Usage & Setup

1. **Clone the Repo**  
```bash
    git clone https://github.com/your-user/janus.git
    cd janus
```
### Install Dependencies

- **Backend:**
    Create a Python virtual environment and install from `requirements.txt` or `pyproject.toml`.

- **Frontend:**
    Install Node.js dependencies (`npm install or yarn`).

### Local Development

- **Backend:** 
    `flask run` or `python backend/app.py`.

- **Frontend:**
    `npm run dev` (Next.js) to serve the UI locally.

### Testing

- **Python tests:**
    `pytest tests/`.

- **Lint checks:**
    `flake8` and `black --check` (or see `backend/utils/code_quality.py`).

### Deployment

- Currently tested with local SQLite; recommended to switch to a more robust DB (e.g., PostgreSQL) in production.

- Plan to host the frontend via Vercel (or any Next.js-friendly provider).

## Roadmap

### Complete Frontend UI

- Finalize atomic design system.
- Integrate automatic theming from analyzed image data.

### Strengthen the Backend

- Implement robust tests for all routes.
- Switch from SQLite to a production DB.
- Expand advanced ML modules for real-time image analysis.

### Deeper Accessibility & AI

- Refine WCAG-based color/luminosity checks, making the site truly inclusive.
- Integrate custom or advanced AI models to handle complex design tasks.

# Contributing
Contributions and suggestions are welcome. Please open an issue or submit a pull request to discuss changes. I aim to maintain clean code (passing Flake8, Black, Pylint) and well-documented commits.


# License
Distributed under the MIT License. You are free to modify or redistribute this software, as long as the original license is retained.

# Final Notes
This project is both personal (a demonstration of my capabilities, creativity, and learning) and community-oriented (open-source with the goal of making design + accessibility more approachable). While some features remain in flux—especially around AI-based design token generation—the ultimate vision is to help developers and designers quickly create interfaces that are both beautiful and inclusive.

```
Thank you for visiting Janus!

If you have any questions or would like to collaborate, feel free to reach out or open a discussion on GitHub.
```