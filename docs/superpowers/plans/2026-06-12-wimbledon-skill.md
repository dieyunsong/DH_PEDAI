# Wimbledon Design System Skill — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a Claude skill that guides any frontend project to adopt the Wimbledon chic aesthetic — dark crimson background, sage green accents, cream type, EB Garamond italic serif headings, Josefin Sans UI labels — outputting design tokens in the correct format for the user's stack (CSS, Tailwind, or JS/TS).

**Architecture:** A three-file skill — `SKILL.md` (orchestration + stack detection logic), `references/tokens.md` (full design token reference), and `references/components.md` (copy-paste component recipes). Claude reads `SKILL.md` on trigger, then loads only the reference file relevant to the user's request.

**Tech Stack:** Plain Markdown skill files installed into the superpowers plugin skills directory. No build step. No dependencies.

---

## File Map

| Action | Path | Responsibility |
|---|---|---|
| Create | `~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/wimbledon-aesthetic/SKILL.md` | Skill entry point: trigger description, stack detection, output rules |
| Create | `~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/wimbledon-aesthetic/references/tokens.md` | Complete design token spec (palette, type scale, spacing, shape) |
| Create | `~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/wimbledon-aesthetic/references/components.md` | Component recipes: nav, card, buttons, badges, input |

---

## Task 1: Write the design token reference

**Files:**
- Create: `~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/wimbledon-aesthetic/references/tokens.md`

- [ ] **Step 1: Create the references directory**

```bash
mkdir -p ~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/wimbledon-aesthetic/references
```

- [ ] **Step 2: Write `references/tokens.md`**

Create the file with this exact content:

```markdown
# Wimbledon Design System — Tokens

## Colour Palette

| Token name | Hex | Role |
|---|---|---|
| crimson | #6b1212 | Primary background, dominant surface |
| strawberry | #8B1A1A | Secondary background, hover states |
| sage | #a8d5a2 | Accent: labels, rule lines, borders, links |
| cream | #fff8f0 | Primary text on dark backgrounds |
| blush | #e8d5c4 | Body text, secondary text on dark |
| midnight | #1a1a1a | Page background behind panels |

**Palette rules (never break these):**
- Background is always a single solid colour — no gradients on surfaces.
- Sage is accent-only — never use it as a background.
- Cream is the headline colour on crimson/strawberry surfaces.
- Blush is body/secondary text on crimson/strawberry surfaces.

## Typography

### Font families

| Token | Value |
|---|---|
| font-serif | 'EB Garamond', Georgia, serif |
| font-sans | 'Josefin Sans', Arial, sans-serif |

**Google Fonts import URL:**
```
https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Josefin+Sans:wght@300;400;600&display=swap
```

### Type scale

| Token | Family | Size | Weight | Style | Line-height | Letter-spacing |
|---|---|---|---|---|---|---|
| text-display | serif | 48px | 400 | italic | 1.1 | 0 |
| text-heading | serif | 28px | 400 | italic | 1.25 | 0 |
| text-subheading | serif | 20px | 400 | normal | 1.4 | 0 |
| text-body | serif | 16px | 400 | normal | 1.7 | 0 |
| text-label | sans | 10px | 300 | normal | 1.4 | 5px |
| text-button | sans | 10px | 600 | normal | 1 | 4px |

**Typography rules:**
- Headings and display text are always italic serif.
- Labels, nav links, and buttons are always Josefin Sans, uppercase, wide letter-spacing.
- Never use bold weight on serif — contrast comes from italic vs roman, not bold.

## Spacing & Shape

| Token | Value |
|---|---|
| radius | 2px (near-flat — no rounded cards) |
| space-xs | 8px |
| space-sm | 16px |
| space-md | 28px |
| space-lg | 48px |
| space-xl | 72px |

**Rule line:** 36–40px wide, 1px tall, sage colour — used between eyebrow label and heading.

## Output Formats

### CSS custom properties
```css
:root {
  /* Colours */
  --color-crimson: #6b1212;
  --color-strawberry: #8B1A1A;
  --color-sage: #a8d5a2;
  --color-cream: #fff8f0;
  --color-blush: #e8d5c4;
  --color-midnight: #1a1a1a;

  /* Typography */
  --font-serif: 'EB Garamond', Georgia, serif;
  --font-sans: 'Josefin Sans', Arial, sans-serif;
  --text-display-size: 48px;
  --text-heading-size: 28px;
  --text-subheading-size: 20px;
  --text-body-size: 16px;
  --text-label-size: 10px;
  --text-label-spacing: 5px;
  --text-button-spacing: 4px;

  /* Spacing */
  --space-xs: 8px;
  --space-sm: 16px;
  --space-md: 28px;
  --space-lg: 48px;
  --space-xl: 72px;
  --radius: 2px;
}
```

### Tailwind config extension
```js
// tailwind.config.js — inside theme.extend
colors: {
  wimbledon: {
    crimson:    '#6b1212',
    strawberry: '#8B1A1A',
    sage:       '#a8d5a2',
    cream:      '#fff8f0',
    blush:      '#e8d5c4',
    midnight:   '#1a1a1a',
  }
},
fontFamily: {
  serif: ["'EB Garamond'", 'Georgia', 'serif'],
  sans:  ["'Josefin Sans'", 'Arial', 'sans-serif'],
},
borderRadius: { DEFAULT: '2px', none: '0' },
letterSpacing: { label: '5px', button: '4px', eyebrow: '7px' },
```

### JS/TS theme object
```ts
export const wimbledon = {
  colors: {
    crimson:    '#6b1212',
    strawberry: '#8B1A1A',
    sage:       '#a8d5a2',
    cream:      '#fff8f0',
    blush:      '#e8d5c4',
    midnight:   '#1a1a1a',
  },
  fonts: {
    serif: "'EB Garamond', Georgia, serif",
    sans:  "'Josefin Sans', Arial, sans-serif",
  },
  spacing: { xs: '8px', sm: '16px', md: '28px', lg: '48px', xl: '72px' },
  radius: '2px',
} as const;
```
```

- [ ] **Step 3: Verify the file was created**

```bash
wc -l ~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/wimbledon-aesthetic/references/tokens.md
```

Expected: 100+ lines.

- [ ] **Step 4: Commit**

```bash
git -C /Users/Dieyun/Documents/DHSI2026/DH_PEDAI add -A
git -C /Users/Dieyun/Documents/DHSI2026/DH_PEDAI commit -m "feat: add wimbledon skill tokens reference"
```

---

## Task 2: Write the component recipes reference

**Files:**
- Create: `~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/wimbledon-aesthetic/references/components.md`

- [ ] **Step 1: Write `references/components.md`**

Create the file with this exact content:

```markdown
# Wimbledon Design System — Component Recipes

All components reference tokens defined in `references/tokens.md`.
Adapt markup/class syntax to the user's stack (plain CSS, Tailwind, or React).

---

## Navigation

**Structure:** logo (italic serif) + spaced nav links (Josefin Sans, sage) + sage accent dot

### Plain CSS + HTML
```html
<nav class="wim-nav">
  <span class="wim-nav__logo">Wimbledon</span>
  <ul class="wim-nav__links">
    <li><a href="#">Schedule</a></li>
    <li><a href="#">Players</a></li>
    <li><a href="#">History</a></li>
  </ul>
  <span class="wim-nav__dot"></span>
</nav>
```
```css
.wim-nav {
  background: var(--color-crimson);
  padding: 18px 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.wim-nav__logo {
  font-family: var(--font-serif);
  font-style: italic;
  font-size: 20px;
  color: var(--color-cream);
}
.wim-nav__links {
  display: flex;
  gap: 28px;
  list-style: none;
}
.wim-nav__links a {
  font-family: var(--font-sans);
  font-size: 9px;
  letter-spacing: 4px;
  text-transform: uppercase;
  color: var(--color-sage);
  text-decoration: none;
  font-weight: 300;
}
.wim-nav__dot {
  width: 4px;
  height: 4px;
  background: var(--color-sage);
  border-radius: 50%;
  display: block;
}
```

---

## Card

**Structure (top to bottom):** eyebrow → heading (italic serif) → rule line → body → optional tags

### Plain CSS + HTML
```html
<article class="wim-card">
  <p class="wim-card__eyebrow">Centre Court</p>
  <h2 class="wim-card__heading">Gentlemen's Singles Final</h2>
  <div class="wim-card__rule"></div>
  <p class="wim-card__body">The most prestigious match in tennis, played on hallowed grass every July.</p>
  <div class="wim-card__tags">
    <span class="wim-tag">Grass Court</span>
    <span class="wim-tag">Grand Slam</span>
  </div>
</article>
```
```css
.wim-card {
  background: var(--color-crimson);
  padding: 32px 28px;
  border-radius: var(--radius);
}
.wim-card__eyebrow {
  font-family: var(--font-sans);
  font-size: 9px;
  letter-spacing: 7px;
  text-transform: uppercase;
  color: var(--color-sage);
  font-weight: 300;
  margin-bottom: var(--space-sm);
}
.wim-card__heading {
  font-family: var(--font-serif);
  font-style: italic;
  font-size: 26px;
  font-weight: 400;
  color: var(--color-cream);
  line-height: 1.25;
  margin-bottom: var(--space-xs);
}
.wim-card__rule {
  width: 36px;
  height: 1px;
  background: var(--color-sage);
  margin-bottom: var(--space-sm);
}
.wim-card__body {
  font-family: var(--font-serif);
  font-size: 14px;
  line-height: 1.7;
  color: var(--color-blush);
  margin-bottom: var(--space-md);
}
.wim-tag {
  display: inline-block;
  font-family: var(--font-sans);
  font-size: 9px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--color-sage);
  border: 1px solid var(--color-sage);
  padding: 4px 10px;
  margin-right: 6px;
}
```

---

## Buttons

### Primary (sage fill, crimson text)
```html
<button class="wim-btn wim-btn--primary">Book Tickets</button>
```
```css
.wim-btn {
  font-family: var(--font-sans);
  font-size: 10px;
  letter-spacing: 4px;
  text-transform: uppercase;
  padding: 12px 28px;
  border: none;
  cursor: pointer;
  border-radius: var(--radius);
  font-weight: 600;
}
.wim-btn--primary {
  background: var(--color-sage);
  color: var(--color-crimson);
}
.wim-btn--primary:hover { background: #c8e8c2; }
```

### Ghost (transparent, sage border + text)
```html
<button class="wim-btn wim-btn--ghost">Learn More</button>
```
```css
.wim-btn--ghost {
  background: transparent;
  color: var(--color-sage);
  border: 1px solid var(--color-sage);
  font-weight: 400;
}
.wim-btn--ghost:hover {
  background: rgba(168, 213, 162, 0.08);
}
```

---

## Badges

### On dark background (crimson bg, sage text)
```html
<span class="wim-badge">Centre Court</span>
```
```css
.wim-badge {
  background: var(--color-crimson);
  color: var(--color-sage);
  font-family: var(--font-sans);
  font-size: 8px;
  letter-spacing: 4px;
  text-transform: uppercase;
  padding: 5px 12px;
  display: inline-block;
  font-weight: 300;
}
```

### Cream badge (cream bg, crimson text)
```html
<span class="wim-badge wim-badge--cream">Grand Slam</span>
```
```css
.wim-badge--cream {
  background: var(--color-cream);
  color: var(--color-crimson);
}
```

---

## Input

Sits on a crimson surface. Bottom-border only, transparent background.

```html
<div class="wim-field">
  <input class="wim-input" type="text" placeholder="Search players…" />
</div>
```
```css
.wim-input {
  background: transparent;
  border: none;
  border-bottom: 1px solid var(--color-sage);
  color: var(--color-cream);
  font-family: var(--font-serif);
  font-size: 16px;
  padding: 8px 0;
  width: 100%;
  outline: none;
}
.wim-input::placeholder {
  color: #a8a8a8;
  font-style: italic;
}
.wim-input:focus {
  border-bottom-color: var(--color-cream);
}
```

---

## Hero Section

Full-width crimson panel with centred display type.

```html
<section class="wim-hero">
  <p class="wim-hero__eyebrow">The Championships</p>
  <h1 class="wim-hero__title">Strawberries &amp; Cream</h1>
  <div class="wim-hero__rule"></div>
  <p class="wim-hero__sub">Centre Court · Since 1877</p>
</section>
```
```css
.wim-hero {
  background: var(--color-crimson);
  padding: var(--space-xl) var(--space-lg);
  text-align: center;
}
.wim-hero__eyebrow {
  font-family: var(--font-sans);
  font-size: 9px;
  letter-spacing: 8px;
  text-transform: uppercase;
  color: var(--color-sage);
  font-weight: 300;
  margin-bottom: var(--space-md);
}
.wim-hero__title {
  font-family: var(--font-serif);
  font-style: italic;
  font-size: 48px;
  font-weight: 400;
  color: var(--color-cream);
  line-height: 1.1;
  margin-bottom: var(--space-sm);
}
.wim-hero__rule {
  width: 40px;
  height: 1px;
  background: var(--color-sage);
  margin: 0 auto var(--space-sm);
}
.wim-hero__sub {
  font-family: var(--font-sans);
  font-size: 10px;
  letter-spacing: 5px;
  text-transform: uppercase;
  color: var(--color-sage);
  font-weight: 300;
}
```
```

- [ ] **Step 2: Verify the file was created**

```bash
wc -l ~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/wimbledon-aesthetic/references/components.md
```

Expected: 200+ lines.

- [ ] **Step 3: Commit**

```bash
git -C /Users/Dieyun/Documents/DHSI2026/DH_PEDAI add -A
git -C /Users/Dieyun/Documents/DHSI2026/DH_PEDAI commit -m "feat: add wimbledon skill component recipes"
```

---

## Task 3: Write the main SKILL.md

**Files:**
- Create: `~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/wimbledon-aesthetic/SKILL.md`

- [ ] **Step 1: Write `SKILL.md`**

Create the file with this exact content:

```markdown
---
name: wimbledon-aesthetic
description: >
  Apply the Wimbledon chic design system to any frontend project. Use this skill whenever
  the user mentions Wimbledon style, chic/elegant aesthetic, strawberries and cream palette,
  dark crimson backgrounds, sage green accents, EB Garamond headings, or wants a tennis/British
  luxury look. Also trigger when the user asks for a design system, theme tokens, or component
  styling and the project already uses this aesthetic. Outputs design tokens in the correct
  format for the user's stack (CSS custom properties, Tailwind config, or JS/TS theme object)
  plus copy-paste component recipes.
---

# Wimbledon Aesthetic Design System

A chic, elegant frontend design system inspired by Wimbledon — dark crimson surfaces, sage green
accents, cream typography, italic Garamond headings, and ultra-light Josefin Sans labels.

## Step 1: Detect the stack

Before outputting anything, check which framework the project uses:

1. Look for `tailwind.config.js` or `tailwind.config.ts` → **Tailwind**
2. Look for `package.json` with React/Vue/Svelte/Next → check for CSS-in-JS (styled-components,
   emotion, stitches) → **JS/TS theme object**
3. Otherwise → **plain CSS custom properties**

If you cannot determine the stack, ask: "Are you using Tailwind, a JS/TS theme object, or plain CSS?"

## Step 2: Read the token reference

Read `references/tokens.md` now. It contains the complete palette, type scale, spacing system,
and ready-to-paste output blocks for all three stack formats.

## Step 3: Output tokens

Paste the correct output block from `references/tokens.md` for the detected stack.
Always include:
- The Google Fonts import URL (remind the user to add it to their HTML `<head>` or CSS entry point)
- The full token block
- A one-line comment above each section explaining what it is

## Step 4: Handle component requests

If the user asks for a specific component (nav, card, button, badge, input, hero), read
`references/components.md` and output the recipe for that component only.

If the user asks for "all components" or "the full system", output all recipes from
`references/components.md`.

Always adapt the markup/class syntax to the user's stack:
- Plain CSS → use the `.wim-*` class recipes as written
- Tailwind → translate CSS properties to utility classes, using `wimbledon.*` colour tokens
- React → wrap in a functional component with inline styles or a CSS module import

## Palette rules — never break these

- Background is always a single solid colour. No gradients on surfaces.
- Sage (`#a8d5a2`) is accent-only — labels, rule lines, borders, links. Never a background.
- Cream (`#fff8f0`) is the headline text colour on crimson/strawberry surfaces.
- Blush (`#e8d5c4`) is body/secondary text on crimson/strawberry surfaces.
- Headings and display text are always italic serif (EB Garamond).
- UI labels, nav links, buttons: always Josefin Sans, uppercase, wide letter-spacing.
- Never use bold weight on serif — contrast comes from italic vs roman, not bold.
```

- [ ] **Step 2: Verify the skill file exists and has the frontmatter**

```bash
head -10 ~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/wimbledon-aesthetic/SKILL.md
```

Expected output starts with `---` and includes `name: wimbledon-aesthetic`.

- [ ] **Step 3: Reload skills to confirm discovery**

In Claude Code, run:
```
/reload-skills
```

Expected: output includes `wimbledon-aesthetic` in the skill list and total count increases by 1.

- [ ] **Step 4: Commit**

```bash
git -C /Users/Dieyun/Documents/DHSI2026/DH_PEDAI add -A
git -C /Users/Dieyun/Documents/DHSI2026/DH_PEDAI commit -m "feat: add wimbledon-aesthetic skill SKILL.md"
```

---

## Task 4: Smoke-test the skill

- [ ] **Step 1: Test token output — plain CSS**

Start a new Claude Code session (or use the current one after `/reload-skills`) and type:

```
I'm building a plain HTML/CSS landing page. Apply the Wimbledon aesthetic design system.
```

Expected: Claude reads the skill, detects plain CSS stack, pastes the `:root {}` CSS custom
properties block, includes the Google Fonts import URL, and explains the palette rules.

- [ ] **Step 2: Test component output**

In the same or a new session, type:

```
Give me the Wimbledon card component.
```

Expected: Claude outputs the `.wim-card` HTML + CSS recipe from `references/components.md`.

- [ ] **Step 3: Test Tailwind output**

Create a temp file to simulate stack detection:

```bash
echo '{"devDependencies":{"tailwindcss":"^3.4.0"}}' > /tmp/wim-test-package.json
```

Then type:

```
My project uses Tailwind CSS (tailwind.config.js present). Apply the Wimbledon aesthetic.
```

Expected: Claude outputs the `theme.extend` Tailwind config block with `wimbledon.*` colour tokens.

- [ ] **Step 4: Commit test notes**

```bash
git -C /Users/Dieyun/Documents/DHSI2026/DH_PEDAI commit --allow-empty -m "test: wimbledon skill smoke test passed"
```

---

## Self-Review

**Spec coverage check:**

| Spec requirement | Covered by |
|---|---|
| Palette: 6 colours with roles | Task 1 tokens.md |
| Palette rules (sage accent-only, single bg) | Task 1 tokens.md + Task 3 SKILL.md |
| Typography: EB Garamond + Josefin Sans | Task 1 tokens.md |
| Type scale: 6 levels | Task 1 tokens.md |
| Spacing & shape tokens | Task 1 tokens.md |
| CSS / Tailwind / JS output formats | Task 1 tokens.md (all three blocks) |
| Stack detection logic | Task 3 SKILL.md Step 1 |
| Nav component | Task 2 components.md |
| Card component | Task 2 components.md |
| Buttons (primary + ghost) | Task 2 components.md |
| Badges (dark + cream) | Task 2 components.md |
| Input component | Task 2 components.md |
| Hero section | Task 2 components.md |
| Skill trigger description | Task 3 SKILL.md frontmatter |

All spec requirements covered. No gaps.
