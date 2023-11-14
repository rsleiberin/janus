# Agent Responsibilities

Each agent within the system has a set of defined responsibilities and associated tasks. Below is a detailed list of these responsibilities and the files and directories each agent will interact with.

## Initialization Agent

**Responsibilities:**
- Set up and manage virtual environments.
- Install and update project dependencies.

**Files and Directories:**
- `venv/`
- `requirements.txt` (If exists, otherwise manage installations directly)

## Backend Agent

**Responsibilities:**
- Initialize the Flask application.
- Set up routing and backend logic.

**Files and Directories:**
- `app.py`
- `config.py`
- `app/blueprints/`

## Design System Agent

**Responsibilities:**
- Apply design principles and elements to the project.
- Ensure UI/UX consistency across the application.

**Files and Directories:**
- `documentation/design_system/design_tokens.md`
- `documentation/design_system/best_practices/`

## Frontend Agent

**Responsibilities:**
- Develop and manage the Next.js frontend.
- Implement Tailwind CSS for styling.

**Files and Directories:**
- `frontend/src/`
- `frontend/styles/`
- `frontend/tailwind.config.js`

## Content Creation Agent

**Responsibilities:**
- Create and manage website content based on design templates.
- Adhere to information architecture guidelines.

**Files and Directories:**
- `app/blueprints/home/templates/`
- `INFORMATION_ARCHITECTURE.md`

## Review and Testing Agent

**Responsibilities:**
- Review the website against design and functional specifications.
- Perform tests to ensure all features are working as intended.

**Files and Directories:**
- `tasklist.md`
- Any test scripts or checklists provided in the project directories.

## Deployment Agent

**Responsibilities:**
- Deploy the website to the production server.
- Manage releases and version control.

**Files and Directories:**
- `utils/`
- Deployment scripts (location to be specified)

**Note:** Each agent must update the respective `README.md` within their directory with a log of changes after completing their tasks.

