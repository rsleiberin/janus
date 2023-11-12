# Backend Design Token Integration

## Introduction
This document outlines Flask-specific processes and best practices for the integration and management of design tokens within the backend environment of our web application.

## Serving Design Tokens via Flask's API

Design tokens are served via a RESTful API, following best practices for security and scalability:

### RESTful API Design

```python
# Flask endpoint for retrieving theming design tokens
@app.route('/api/design_tokens/themes', methods=['GET'])
def get_themes():
    # Load design tokens from a JSON file
    with open('design_tokens/themes.json', 'r') as f:
        themes = json.load(f)
    return jsonify(themes)
```

## API Versioning

```python
# Versioned API endpoint for theming design tokens
@app.route('/api/v1/design_tokens/themes', methods=['GET'])
def get_themes_v1():
    # Logic for Version 1 API for themes
    pass
```

For more details on API design and versioning, refer to the comprehensive guide in `./design_token_system.md`

## Dynamic Design Token Manipulation in Flask
Leverage Flask-Assets and Jinja2 to enable dynamic token updates within the templating system:

### Flask-Assets Integration

```python
# Setup Flask-Assets to compile and serve assets
from flask_assets import Environment, Bundle

assets = Environment(app)

# Define and configure asset bundles
js = Bundle('src/js/app.js', filters='jsmin', output='dist/js/app.min.js')
css = Bundle('src/css/style.scss', filters='scss', cssmin', output='dist/css/style.min.css')

assets.register('js_all', js)
assets.register('css_all', css)
```

### Jinja2 Templating with Autoversioning

```html
<!-- Jinja2 template example with an autoversioning filter for stylesheet link -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') | autoversion }}">
```

### Autoversion Filter

```python
# Flask template filter for asset autoversioning to handle cache busting
@app.template_filter('autoversion')
def autoversion_filter(filename):
    # Build the full path for the filename
    fullpath = os.path.join('app/static', filename)
    # Extract the last modified timestamp for versioning
    timestamp = str(os.path.getmtime(fullpath))
    # Append the timestamp to the filename as a query string
    new_filename = f"{filename}?v={timestamp}"
    return url_for('static', filename=new_filename)
```

This document provides a more detailed look at Flask-specific best practices for design tokens. For more in-depth information and broader guidelines on the design token system, please refer to `./design_token_system.md`.
