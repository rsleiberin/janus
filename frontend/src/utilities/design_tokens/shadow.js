// Shadow Token File
// This file defines the shadow tokens used across the design system. 
// Shadow tokens are used to add depth, focus, and hierarchy to the interface, enhancing the user experience.

const shadowToken = {
    // Elevation Levels: Define the shadow depth based on UI component elevation.
    // These levels help in creating a visual hierarchy and focus areas in the UI.
    elevation: {
      // Sunken: Lowest elevation, typically used for backdrops or wells, where other content is placed on top.
      // Example usage: Backgrounds for sections or containers where content appears to be inset.
      sunken: {
        shadow: 'none' // No shadow for sunken elements to simulate depth into the page.
      },
  
      // Default: Standard elevation for most UI components.
      // Example usage: Cards, buttons, or any element that needs a subtle lift off the page.
      default: {
        shadow: '0px 1px 3px rgba(0, 0, 0, 0.2)' // Soft shadow for a gentle elevation.
      },
  
      // Raised: Higher elevation for elements that need to stand out.
      // Example usage: Modals, pop-up menus, or floating action buttons.
      raised: {
        shadow: '0px 4px 6px rgba(0, 0, 0, 0.3)' // More pronounced shadow for elements that should float above others.
      },
  
      // Overlay: Highest elevation, used for elements that must be prominently above all other content.
      // Example usage: Alerts, overlays, or crucial floating elements.
      overlay: {
        shadow: '0px 8px 10px rgba(0, 0, 0, 0.4)' // Strongest shadow to create a clear distinction from the rest of the UI.
      }
    }
  };
  
  // Export the shadowToken for consistent use across the design system.
  // This ensures that all components adhere to the same depth and focus standards, maintaining design consistency.
  export default shadowToken;
  