# Design Token Category Library

## Color Tokens

### Base Palette
- `dark-base`: #121212, #1D1D1D, #242424 (Dark Mode Backgrounds)
- `light-base`: #FFFFFF, #F0F0F0, #E1E1E1 (Light Mode Backgrounds)
- `text-dark`: #E8E8E8, #C0C0C0 (Dark Mode Text)
- `text-light`: #333333, #4F4F4F (Light Mode Text)

### Accent Colors
- `primary`: #BB86FC, #3700B3 (Dark), #6200EE (Light)
- `secondary`: #03DAC6, #018786 (Dark), #03DAC5 (Light)
- `feedback`: #CF6679 (Errors), #FFDD57 (Warnings), #03DAC6 (Success)

### Semantic Colors
- `error-dark`: #CF6679, `error-light`: #B00020
- `warning-dark`: #FFDD57, `warning-light`: #C7971E
- `success-dark`: #03DAC6, `success-light`: #018786
- `info-dark`: #03A9F4, `info-light`: #0288D1

## Typography Tokens

### Font Families
- `primary-font`: "Inter", "San Francisco", "Roboto", sans-serif
- `code-font`: "Source Code Pro", monospace

### Font Sizes
- `font-size-root`: 16px
- `font-size-scale`: 12px, 14px, 16px, 20px, 24px, 32px

### Font Weights
- `font-weight-regular`: 400
- `font-weight-medium`: 500
- `font-weight-bold`: 700

### Line Heights
- `line-height-tight`: 1.2
- `line-height-base`: 1.5
- `line-height-relaxed`: 1.75

## Spacing Tokens

### Scale
- `space-unit`: 8px
- `space-scale`: 4px, 8px, 16px, 24px, 32px, 48px

### Responsive Spacing
- `space-responsive`: `space-scale` mapped to media queries

## Border and Corner Tokens

### Border Width
- `border-width-none`: 0
- `border-width-thin`: 1px
- `border-width-thick`: 2px

### Border Styles
- `border-style-solid`: solid
- `border-style-dashed`: dashed
- `border-style-dotted`: dotted

### Radius Tokens
- `radius-small`: 2px
- `radius-medium`: 4px
- `radius-large`: 8px
- `radius-round`: 9999px

## Elevation Tokens

### Box Shadows
- `shadow-1`: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)
- `shadow-2`: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23)

### Layering Z-Index
- `z-index-default`: 1
- `z-index-dropdown`: 1000
- `z-index-sticky`: 1020
- `z-index-modal`: 1050

## Motion Tokens

### Transition Durations
- `duration-fast`: 200ms
- `duration-normal`: 300ms
- `duration-slow`: 500ms

### Easing Functions
- `easing-linear`: linear
- `easing-ease-in`: cubic-bezier(0.4, 0, 1, 1)
- `easing-ease-out`: cubic-bezier(0, 0, 0.2, 1)
- `easing-ease-in-out`: cubic-bezier(0.4, 0, 0.2, 1)

## Component Tokens

### Button Styles
- `button-primary`: `primary` color, `font-weight-bold`
- `button-secondary`: `secondary` color, `font-weight-regular`

### Form Elements
- `input-text`: `border-width-thin`, `radius-small`
- `select-menu`: `border-width-thin`, `radius-medium`
- `toggle-slider`: `radius-round`

## Breakpoint Tokens

### Screen Sizes
- `screen-xs`: "only screen and (max-width: 639px)"
- `screen-sm`: "only screen and (min-width: 640px)"
- `screen-md`: "only screen and (min-width: 768px)"
- `screen-lg`: "only screen and (min-width: 1024px)"
- `screen-xl`: "only screen and (min-width: 1280px)"

## Iconography Tokens

### Icon Sizes
- `icon-size-xs`: 12px
- `icon-size-sm`: 16px
- `icon-size-md`: 24px
- `icon-size-lg`: 32px
- `icon-size-xl`: 48px

### Icon Styles
- `icon-style-line`: stroke-based
- `icon-style-solid`: fill-based

## Opacity Tokens

### Opacity Scale
- `opacity-0`: 0%
- `opacity-50`: 50%
- `opacity-100`: 100%

## Animation Tokens

### Animation Types
- `animation-fade`: opacity transition
- `animation-slide`: translation along X or Y axis
- `animation-bounce`: scale transition

### Animation Timings
- `animation-duration`: 250ms, 500ms, 750ms
- `animation-delay`: none, short (50ms), long (100ms)

## Grid and Layout Tokens

### Container Widths
- `container-max-xs`: 100%
- `container-max-sm`: 640px
- `container-max-md`: 768px
- `container-max-lg`: 1024px
- `container-max-xl`: 1280px

### Gutter Widths
- `gutter-width-xs`: 16px
- `gutter-width-sm`: 24px
- `gutter-width-md`: 32px
- `gutter-width-lg`: 48px
- `gutter-width-xl`: 64px

Citations:
- [20 Best Design System Examples | Built In](https://builtin.com/design/20-best-design-system-examples)