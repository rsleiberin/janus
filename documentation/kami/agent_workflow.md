# Agent Workflow

This document outlines the sequence and interaction of agents in the website building process.

## Workflow Sequence

1. **Initialization Agent**:
   - Prepares the environment, sets up virtual environments, and installs dependencies.
   - Accesses `config.py` to configure the backend settings.
   
2. **Backend Agent**:
   - Initiates the Flask application using `app.py`.
   - Utilizes the `blueprints/` for routing and views.
   
3. **Design System Agent**:
   - Applies design tokens from `design_system/` to ensure consistent styling.
   - References `best_practices/` to align with the latest UI/UX standards.

4. **Frontend Agent**:
   - Builds the user interface in `frontend/` using components from `src/`.
   - Styles the interface with Tailwind CSS according to `tailwind.config.js`.

5. **Content Creation Agent**:
   - Populates the website with content, using `templates/` in the frontend for layout.
   - Ensures content adheres to `INFORMATION_ARCHITECTURE.md` guidelines.

6. **Review and Testing Agent**:
   - Reviews the website for adherence to design and functional specifications.
   - Conducts testing based on `tasklist.md` to ensure all functionalities work.

7. **Deployment Agent**:
   - Handles the deployment of the website to the production environment.
   - Manages version control and deployment scripts in the `utils/` directory.

## File and Folder Access

Each agent is granted access to specific directories and files as needed for their tasks. Temporary access is managed through an access control system, ensuring agents only have the permissions necessary for their operation.

## Agent Interaction

Agents pass control to the next in sequence after completing their tasks, with the output of one agent becoming the input for another. This hand-off is documented and managed through a centralized task management system, ensuring a smooth workflow.

