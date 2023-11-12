# Developer Guidelines for Using the Design Token System

The design token system is a collection of reusable variables that define our visual design language. Here's how to implement and use these tokens in our web application.

## Working with Design Tokens in Flask

When working on the backend, use the design tokens defined in `design-tokens.json` to style server-rendered templates and API responses.

\```python
# Example of using design tokens in a Flask route
from flask import render_template
import json

@app.route('/some-page')
def some_page():
    with open('design-tokens.json') as f:
        tokens = json.load(f)
    return render_template('some-page.html', tokens=tokens)
\```

Ensure that all Flask routes serving HTML content are using the design tokens for consistency.

## Applying Design Tokens in Next.js

Frontend developers should use the `useDesignTokens` hook to access and apply design tokens within components.

\```javascript
// Example of using design tokens in a Next.js component
import useDesignTokens from '../hooks/useDesignTokens';

export default function SomeComponent() {
    const tokens = useDesignTokens();
    
    return (
        <div style={{ color: tokens.colors.primary }}>
            {/* Component content */}
        </div>
    );
}
\```

Remember to handle loading states appropriately when tokens are being fetched from the backend.

## Updating and Adding New Design Tokens

To update or add new design tokens:

1. Modify the `design-tokens.json` file with the new values or additions.
2. Ensure that the Flask backend serves the updated tokens.
3. Update the Tailwind CSS configuration if needed to reflect the changes.
4. Rebuild your frontend to apply the new token values.

## Testing Strategy for Design Tokens

Develop a set of unit and integration tests to validate the application of design tokens. Use visual regression testing tools to catch styling issues before they reach production.

## Best Practices

- Keep design tokens synchronized between the backend and frontend.
- Use clear, descriptive names for design tokens.
- Regularly review the design token system for opportunities to refine and improve.

This documentation should be kept up-to-date as the design token system evolves and as new tokens are added or existing ones are modified.
