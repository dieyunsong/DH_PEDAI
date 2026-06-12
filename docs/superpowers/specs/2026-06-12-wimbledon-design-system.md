# Wimbledon Design System — Spec

**Date:** 2026-06-12
**Direction:** Red D — dark crimson background, sage green accents, cream type
**Aesthetic:** Chic, elegant, Wimbledon-inspired. Strawberries & cream energy. Palatino/Garamond italic serif for display, Josefin Sans for UI labels.

---

## 1. Colour Palette

| Token | Hex | Role |
|---|---|---|
| `--color-crimson` | `#6b1212` | Primary background, dominant surface |
| `--color-strawberry` | `#8B1A1A` | Secondary background, hover states |
| `--color-sage` | `#a8d5a2` | Accent: labels, rule lines, borders, links |
| `--color-cream` | `#fff8f0` | Primary text on dark backgrounds |
| `--color-blush` | `#e8d5c4` | Body text, secondary text on dark |
| `--color-midnight` | `#1a1a1a` | Page background behind panels |

**Rules:**
- Background is always a single solid colour — no gradients on surfaces.
- Sage green never appears as a background; it is accent-only.
- Cream is the headline text colour on crimson or strawberry surfaces.
- Blush is body/secondary text on crimson or strawberry surfaces.

---

## 2. Typography

### Font Families

| Token | Value | Role |
|---|---|---|
| `--font-serif` | `'EB Garamond', Georgia, serif` | All headings, display, body copy |
| `--font-sans` | `'Josefin Sans', Arial, sans-serif` | UI labels, nav links, badges, buttons |

**Google Fonts import:**
```
https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Josefin+Sans:wght@300;400;600&display=swap
```

### Type Scale

| Token | Family | Size | Weight | Style | Line-height | Letter-spacing |
|---|---|---|---|---|---|---|
| `--text-display` | serif | 48px | 400 | italic | 1.1 | 0 |
| `--text-heading` | serif | 28px | 400 | italic | 1.25 | 0 |
| `--text-subheading` | serif | 20px | 400 | normal | 1.4 | 0 |
| `--text-body` | serif | 16px | 400 | normal | 1.7 | 0 |
| `--text-label` | sans | 10px | 300 | normal | 1.4 | 5px |
| `--text-button` | sans | 10px | 600 | normal | 1 | 4px |

**Rules:**
- Headings and display text are always italic serif.
- Labels, nav links, and buttons are always Josefin Sans, uppercase, wide letter-spacing.
- Never use bold serif — weight contrast comes from italic vs roman, not bold.

---

## 3. Spacing & Shape

| Token | Value |
|---|---|
| `--radius` | `2px` (near-flat — no rounded cards) |
| `--space-xs` | `8px` |
| `--space-sm` | `16px` |
| `--space-md` | `28px` |
| `--space-lg` | `48px` |
| `--space-xl` | `72px` |

**Rule line:** `width: 36–40px; height: 1px; background: var(--color-sage)` — used between eyebrow and heading in cards and hero sections.

---

## 4. Component Patterns

### Navigation
- Background: `--color-crimson`
- Logo: italic serif, `--color-cream`, 20px
- Links: Josefin Sans 300, `--color-sage`, 9px, letter-spacing 4px, uppercase
- Accent dot: 4×4px circle in `--color-sage`

### Card
Structure (top to bottom):
1. **Eyebrow** — Josefin Sans 300, `--color-sage`, 9px, letter-spacing 7px, uppercase
2. **Heading** — EB Garamond italic, `--color-cream`, 26px
3. **Rule line** — sage, 36px wide, 1px tall
4. **Body** — EB Garamond roman, `--color-blush`, 14px, lh 1.7
5. **Tags** (optional) — Josefin Sans, `--color-sage`, 9px, 1px sage border, inline-block

### Buttons
- **Primary**: `background: --color-sage; color: --color-crimson` — Josefin Sans 600, 10px, ls 4px, uppercase, no border-radius
- **Ghost**: `background: transparent; color: --color-sage; border: 1px solid --color-sage` — same type treatment

### Badges
- **On crimson**: `background: --color-crimson; color: --color-sage; border: none` — Josefin Sans 300, 8px, ls 4px, uppercase
- **On dark**: `background: --color-cream; color: --color-crimson` — same type treatment

### Input
- No box border — bottom border only: `border-bottom: 1px solid --color-sage`
- Background: transparent (sits on crimson surface)
- Text: EB Garamond, `--color-cream`, 16px
- Placeholder: italic, `#a8a8a8`

---

## 5. Skill Behaviour

When invoked, the skill should:

1. **Detect the user's stack** — check for `tailwind.config`, `package.json` deps, or file extensions to determine CSS, Tailwind, or JS/TS framework.
2. **Output tokens in the right format:**
   - CSS → custom properties in `:root {}`
   - Tailwind → `theme.extend` block in `tailwind.config.js`
   - JS/TS → exported theme object
3. **Provide component recipes** — for each component the user mentions, output the markup + styles using the token system above.
4. **Never break the palette rules** — sage is accent-only, background is always a single solid colour, headings are always italic serif.

---

## 6. Out of Scope

- Dark/light mode switching (this is a fixed-dark aesthetic)
- Animation or motion design
- Icon system
- Data visualisation components
