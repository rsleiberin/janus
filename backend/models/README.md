# Models Directory

## Overview

The `models/` directory contains all SQLAlchemy model definitions for the Janus backend application. Each model is encapsulated within its own module, promoting modularity and ease of maintenance. Common attributes and behaviors are centralized in the `BaseModel` to adhere to the DRY (Don't Repeat Yourself) principle.

## Structure

- **`__init__.py`**  
  Initializes the `models` package and imports all models for easy access.

- **`base.py`**  
  Defines the `BaseModel`, an abstract class that includes common fields shared across all models, such as `id`, `created_at`, and `updated_at`.

- **`user.py`**  
  Defines the `User` model, including secure password handling methods.

- **`admin.py`**  
  Defines the `Admin` model, which extends the `User` model to include administrative privileges.

- **`image.py`**  
  Defines the `Image` model, which stores metadata about uploaded images and establishes relationships with users.

- **`image_analysis.py`**  
  Defines the `ImageAnalysis` model, which stores analysis results linked to images.

- **`log.py`**  
  Defines the `Log` model, which records user actions and system events.

- **`analytics.py`**  
  Defines the `Analytics` model, which stores research and analytical data relevant to the application's objectives.

- **`security.py`**  
  Defines the `Security` model, which logs security-related events for users.

## Best Practices

- **Modular Design:** Each model is contained within its own module, facilitating easier navigation and maintenance.

- **BaseModel Usage:** Shared attributes and methods are defined in `BaseModel` to reduce redundancy and ensure consistency across models.

- **Secure Password Handling:** The `User` model includes methods for hashing and verifying passwords using secure hashing algorithms.

- **Relationship Management:** Relationships between models are clearly defined using SQLAlchemy's `db.relationship` and `db.ForeignKey` to maintain data integrity.

## Future Development

- **Additional Models:** New models should follow the existing structure, inheriting from `BaseModel` and being placed within their own modules.

- **Refactoring Existing Models:** If models become too complex or numerous, consider further categorizing them into subdirectories based on functionality or domain.

- **Data Validation:** Implement additional data validation either within models or using external libraries to enhance data integrity.

## Contribution Guidelines

- **Naming Conventions:** Use clear and consistent naming conventions for model classes and their corresponding modules.

- **Documentation:** Each model should include a docstring explaining its purpose and relationships.

- **Testing:** Ensure that new models are accompanied by appropriate tests to verify their functionality and relationships.

## Contact

For any questions or contributions related to the models, please reach out to the development team or open an issue in the project's repository.

