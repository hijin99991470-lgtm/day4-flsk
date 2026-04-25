---
name: Lume Editorial
colors:
  surface: '#fff8f4'
  surface-dim: '#e0d9d4'
  surface-bright: '#fff8f4'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#faf2ed'
  surface-container: '#f4ede7'
  surface-container-high: '#eee7e2'
  surface-container-highest: '#e8e1dc'
  on-surface: '#1e1b18'
  on-surface-variant: '#4d453c'
  inverse-surface: '#33302d'
  inverse-on-surface: '#f7efea'
  outline: '#7f766a'
  outline-variant: '#d1c5b8'
  surface-tint: '#725a39'
  primary: '#725a39'
  on-primary: '#ffffff'
  primary-container: '#d3b48c'
  on-primary-container: '#5b4526'
  inverse-primary: '#e1c199'
  secondary: '#5e604d'
  on-secondary: '#ffffff'
  secondary-container: '#e0e1c9'
  on-secondary-container: '#626451'
  tertiary: '#5e5f5d'
  on-tertiary: '#ffffff'
  tertiary-container: '#b9b9b6'
  on-tertiary-container: '#484a48'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffddb3'
  primary-fixed-dim: '#e1c199'
  on-primary-fixed: '#291801'
  on-primary-fixed-variant: '#594324'
  secondary-fixed: '#e3e4cc'
  secondary-fixed-dim: '#c7c8b1'
  on-secondary-fixed: '#1b1d0e'
  on-secondary-fixed-variant: '#464836'
  tertiary-fixed: '#e3e2e0'
  tertiary-fixed-dim: '#c7c6c4'
  on-tertiary-fixed: '#1a1c1a'
  on-tertiary-fixed-variant: '#464745'
  background: '#fff8f4'
  on-background: '#1e1b18'
  surface-variant: '#e8e1dc'
typography:
  h1:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.02em
  h2:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: 0.02em
  caption:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-padding: 20px
  section-margin: 32px
  stack-gap: 16px
  inner-padding: 12px
  toolbar-safe-area: 96px
---

## Brand & Style
Lume is an editorial platform designed for deep focus and mindful storytelling. The brand personality is "Quietly Sophisticated"—it aims to evoke the calm, tactile feeling of high-quality stationery and physical journals. 

The design style is **Minimalist / Modern Editorial**, characterized by generous whitespace, a warm neutral palette, and a focus on typographic hierarchy over heavy UI decoration. It prioritizes the writer's "flow state" by using soft, low-contrast container boundaries and subtle glassmorphic effects in fixed toolbars.

## Colors
The palette is rooted in "New Neutrals"—shifting away from clinical grays toward warm, organic tones like parchment, stone, and tan. 

- **Primary & Secondary:** Use deep earth tones (#725a39 and #5e604d) for interactive elements and highlights to maintain a sophisticated, grounded feel.
- **Backgrounds:** The primary background uses a soft off-white (#FAF9F6) to reduce eye strain during long writing sessions.
- **Semantic Usage:** Use low-contrast variants for decorative dividers and secondary buttons to ensure they don't distract from the primary content (the text).

## Typography
The system uses **Inter** throughout, leveraging its clean, systematic nature to provide a "utilitarian-chic" look. 

- **Titles:** Large titles (H1) use heavy weights and negative letter spacing to create a strong editorial presence.
- **Reading Experience:** The `body-lg` level is the primary writing/reading size, utilizing a generous line height (1.55x) for maximum legibility.
- **Functional UI:** Labels and navigation items use `label-sm` and `caption` sizes with increased letter spacing to maintain clarity at smaller scales.

## Layout & Spacing
The layout follows a **Fixed-Width Content Column** model within a responsive shell. The central writing area is capped at `768px` (md) to ensure comfortable line lengths for reading.

- **Vertical Rhythm:** Large gaps (`section-margin`) separate major conceptual blocks (Hero, Title, Body).
- **Toolbars:** Bottom navigation and formatting toolbars use `fixed` positioning with `backdrop-blur` to float above the content without feeling heavy.
- **Margins:** Standardize on `20px` for mobile container edges.

## Elevation & Depth
Elevation is achieved through a mix of **Tonal Layering** and **Soft Ambient Shadows**.

- **Level 0 (Base):** Background parchment color.
- **Level 1 (Floating/Interactive):** Used for toolbars and primary action buttons. Features a multi-layered shadow (e.g., `shadow-lg`) with a slight warm tint to match the tan seed color.
- **Glassmorphism:** Navigation bars and toolbars utilize 90% opacity with a blur (12px+) to maintain context of the content scrolling underneath.
- **Dividers:** Instead of heavy lines, use 1px borders with 20% opacity of the `outline-variant` color.

## Shapes
The shape language is modern and approachable, using **Rounded** corners to soften the professional typography.

- **Standard Elements:** Buttons and input fields use a base `0.5rem` (8px) radius.
- **Large Containers:** Hero images and card containers use `0.75rem` (12px).
- **Floating UI:** Floating toolbars and chips use a `full` (pill-shaped) radius to distinguish them as high-interaction, tactile objects.

## Components
- **Buttons:** Primary buttons are large and high-contrast (Tan/Brown). Secondary buttons (chips) use `surface-container-low` with no border.
- **Input Fields:** Writing inputs are "invisible"—no borders or backgrounds until focused, allowing the content to be the center of attention.
- **Floating Toolbar:** A pill-shaped bar with high-blur backdrop, featuring icon-only buttons for formatting. Icons should use the `Material Symbols Outlined` set.
- **Chips:** Small, pill-shaped tags used for metadata (tags, visibility). They should have a subtle hover state change (lightening the background).
- **Navigation:** Bottom nav uses a distinct active state with a soft background highlight behind the icon/text pairing.