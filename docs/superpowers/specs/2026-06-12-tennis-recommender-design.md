# Tennis Tournament Recommender — Design Spec
**Date:** 2026-06-12
**Status:** Approved

## Overview

A self-contained single-file HTML app (`tennis-recommender.html`) that guides users through a personality- and style-based quiz — where answer options are real ATP/WTA players — and outputs a calendar view of recommended tennis tournaments. Styled with the Wimbledon aesthetic (dark crimson, sage, cream, EB Garamond). No server, no dependencies, runs by double-clicking.

## Scope

- Top 100 ATP + top 100 WTA players encoded as data objects with dimension scores
- ~40 tournaments at 250-level and above (ATP 250+, WTA 250+, Grand Slams, Masters/1000s)
- No Challengers or lower-level events

---

## Data Model

### Player object
```js
{
  name: "Carlos Alcaraz",
  tour: "ATP",            // "ATP" | "WTA"
  rank: 2,
  scores: {
    forehand: 9,          // 1–10 per dimension
    serve: 7,
    slice: 5,
    mindset: 8,
    humor: 7,
    style: 9,
    doubles: 8
  }
}
```

### Tournament object
```js
{
  name: "Wimbledon",
  surface: "grass",       // "hard" | "clay" | "grass"
  prestige: "grand-slam", // "grand-slam" | "masters" | "500" | "250"
  month: 6,
  week: 25,               // ISO week, for calendar placement
  tour: "both",           // "ATP" | "WTA" | "both"
  vibe: {
    mindset: 8,
    style: 9,
    humor: 5,
    forehand: 6,
    serve: 7,
    slice: 8,
    doubles: 7
  }
}
```

---

## Application Flow

### Screen 1 — Category Picker
- 7 dimension tiles displayed in a grid
- Dimensions: Forehand, Serve, Slice/Net, Mindset, Humor & Personality, Personal Style, Doubles Vibes
- User selects 2–5 categories; selected tiles highlight in sage (`#a8d5a2`)
- "Start Quiz" button activates only when ≥2 categories are selected

### Screen 2 — Quiz Questions
- For each selected category: 3 questions
- Each question presents 4 players as answer cards (mix of ATP and WTA)
- Selecting a player adds their dimension scores (weighted) to a running `userVector`
- Progress bar at top shows question N of total
- Back/Next navigation between questions

### Screen 3 — Calendar Results
- Horizontal 12-month timeline
- Recommended tournaments pinned to their month as cards
- Color-coded by prestige:
  - Grand Slam → crimson background (`#6b1212`)
  - Masters/1000 → strawberry (`#8B1A1A`)
  - 500-level → sage outline (`#a8d5a2`)
  - 250-level → blush outline (`#e8d5c4`)
- Top 3 matches receive a "Best Match" badge
- Clicking a tournament card expands a detail panel: surface, prestige, typical attendees, match score

---

## Scoring Algorithm

1. Each quiz answer adds the selected player's scores for the active dimension to `userVector` (running sum, later normalized)
2. `userVector` is normalized to a unit vector after all questions
3. Each tournament's `vibe` vector is similarly normalized
4. Score = cosine similarity between `userVector` and `tournament.vibe`
5. Prestige bonus: grand-slam +0.1, masters +0.05 (slight nudge toward marquee events)
6. Tournaments ranked by final score; all shown on calendar, top 3 badged

---

## Visual Design

Uses the Wimbledon design system throughout:

| Token | Value |
|---|---|
| Primary surface | `--color-crimson: #6b1212` |
| Secondary surface / hover | `--color-strawberry: #8B1A1A` |
| Accent (borders, links, selected) | `--color-sage: #a8d5a2` |
| Headline text | `--color-cream: #fff8f0` |
| Body text | `--color-blush: #e8d5c4` |
| Page background | `--color-midnight: #1a1a1a` |
| Headings | EB Garamond, italic, never bold |
| Labels / buttons / nav | Josefin Sans, uppercase, wide tracking |

Player answer cards: avatar (initials circle), name, tour badge (ATP/WTA).
Screens transition with a simple CSS fade.

---

## File Structure

```
DH_PEDAI/
└── tennis-recommender.html   # single self-contained file
```

All CSS embedded in `<style>`, all JS embedded in `<script>`, all data in JS constants at top of script block.

---

## Out of Scope

- Live rankings or real-time data fetching
- Challenger / ITF events
- User accounts or saved preferences
- Mobile-specific layout (desktop-first, reasonable on tablet)
