---
name: design-reference
description: |
  Curated collection of 58 DESIGN.md files from real-world products.
  Each DESIGN.md is a complete design system spec (colors, typography, components, layout, shadows, do's/don'ts, agent prompts)
  that AI agents can read to generate pixel-perfect, brand-consistent UI.
  Use when the user wants to build UI that matches a specific product's visual style,
  or needs design system reference for frontend development.
---

# Design Reference — AI-Readable Design Systems

58 real-world design system specs, each a complete DESIGN.md that an AI agent can read to generate consistent UI.

## What is DESIGN.md?

A DESIGN.md is a structured design system document written in Markdown, designed specifically for AI agents to consume. It contains everything needed to reproduce a product's visual identity:

- Visual theme & atmosphere
- Color system (semantic names + hex values + functional roles)
- Typography (font families, full type scale)
- Component styles (buttons, cards, inputs, navigation — with states)
- Layout principles (spacing system, grid, whitespace philosophy)
- Depth & elevation (shadow system, surface hierarchy)
- Do's and Don'ts (design guardrails)
- Responsive behavior (breakpoints, touch targets, collapse strategy)
- Agent Prompt Guide (ready-to-use prompts for AI)

## How to Use

### Quick Start

1. Find the target style from the index below
2. Read the DESIGN.md file from `design-md/<name>/DESIGN.md`
3. Apply the design tokens and principles to the user's project

### Example Workflow

```
User: "帮我做一个类似 Linear 风格的看板页面"

→ Read design-md/linear.app/DESIGN.md
→ Extract color palette, typography, component specs
→ Generate UI using those exact tokens
```

### When to Use This Skill

- User wants UI that looks like a specific product
- User needs design system reference for a project
- User asks "what colors/typography does X use?"
- Building a design system from scratch and needs inspiration
- User wants consistent UI across AI-generated pages

## Design System Index

### AI & ML Platforms

| Product | Style Keywords | Lines |
|---------|---------------|-------|
| `claude` | Warm sand/stone palette, friendly serif + clean sans, approachable AI | 312 |
| `cohere` | Coral accent, clean enterprise, command-line aesthetic | 266 |
| `mistral.ai` | Deep navy + orange accent, French engineering precision | 261 |
| `ollama` | Llama mascot green, playful gradient, open-source community | 267 |
| `x.ai` | Stark minimalism, black/white, Grok's rebellious tone | 257 |
| `together.ai` | Purple gradient, research-lab aesthetic, API-first | 263 |
| `minimax` | Vibrant multi-color, Chinese AI platform, youthful energy | 257 |
| `elevenlabs` | Audio waveform purple, voice-tech dark mode, sound visualization | 265 |
| `replicate` | Orange accent, ML model marketplace, developer playground | 261 |
| `nvidia` | Green + black, GPU power aesthetic, deep-tech authority | 293 |
| `runwayml` | Creative purple, video-gen dark UI, artistic tool | 244 |

### Developer Tools & Infrastructure

| Product | Style Keywords | Lines |
|---------|---------------|-------|
| `vercel` | Geist font, shadow-as-border, extreme minimalism, black/white | 310 |
| `linear.app` | Indigo accent, dense data UI, keyboard-first, precision | 367 |
| `cursor` | Code-editor dark, syntax-highlighted, developer-native | 309 |
| `supabase` | Emerald green, database aesthetic, dashboard UI | 255 |
| `stripe` | Indigo/purple gradient, payment authority, illustrated docs | 322 |
| `mongodb` | Green leaf, database ecosystem, developer hub | 266 |
| `clickhouse` | Yellow accent, high-performance DB, engineering rigor | 281 |
| `hashicorp` | Purple/teal, infrastructure-as-code, enterprise devtools | 278 |
| `sentry` | Pink/magenta, error-tracking urgency, dark mode default | 262 |
| `posthog` | Purple accent, product analytics, playful data viz | 256 |
| `raycast` | Gradient purple, macOS-native feel, command palette | 268 |
| `warp` | Blue/purple gradient, modern terminal, GPU-accelerated | 253 |
| `expo` | Dark navy, React Native ecosystem, mobile-first | 281 |
| `opencode.ai` | Clean minimal, open-source coding, community-driven | 281 |
| `composio` | Gradient accent, AI tool integration, developer platform | 307 |
| `lovable` | Warm gradient, AI app builder, approachable creator tool | 298 |
| `sanity` | Red/coral accent, content studio, structured content | 357 |
| `resend` | Clean minimal, email API, developer communication | 303 |
| `mintlify` | Clean docs aesthetic, documentation platform, purple accent | 326 |
| `zapier` | Orange accent, automation platform, workflow builder | 328 |
| `voltagent` | Agent framework, AI-native design, structured UI | 323 |

### Design & Productivity Tools

| Product | Style Keywords | Lines |
|---------|---------------|-------|
| `figma` | Multi-color, design-tool UI, canvas-centric, collaborative | 220 |
| `framer` | Purple gradient, web design tool, visual builder | 246 |
| `notion` | Clean minimal, productivity workspace, warm neutrals | 309 |
| `airtable` | Colorful grid, no-code database, playful enterprise | 89 |
| `miro` | Yellow accent, collaborative whiteboard, infinite canvas | 108 |
| `webflow` | Blue accent, visual web builder, designer-friendly | 92 |
| `clay` | Warm earth tones, social CRM, relationship-first | 304 |
| `intercom` | Blue/teal, customer messaging, SaaS dashboard | 146 |
| `superhuman` | Purple accent, email client, speed-obsessed, keyboard-first | 252 |
| `cal` | Clean scheduling, calendar UI, minimal friction | 259 |
| `pinterest` | Red accent, visual discovery, masonry grid, warm | 230 |
| `spacex` | Dark mode, space-tech aesthetic, mission control | 194 |
| `ibm` | Blue monolith, enterprise authority, carbon design system | 332 |
| `apple` | Ultra-clean, SF Pro, restrained luxury, white space | 313 |

### Finance & Crypto

| Product | Style Keywords | Lines |
|---------|---------------|-------|
| `coinbase` | Blue accent, crypto exchange, trust & security | 129 |
| `kraken` | Purple accent, crypto trading, dark mode power user | 125 |
| `revolut` | Purple gradient, neobank, fintech minimalism | 185 |
| `wise` | Green accent, money transfer, friendly finance | 173 |

### Automotive

| Product | Style Keywords | Lines |
|---------|---------------|-------|
| `bmw` | Blue/white, precision engineering, luxury performance | 180 |
| `ferrari` | Rosso corsa red, Italian luxury, racing heritage | 314 |
| `lamborghini` | True black + gold, aggressive luxury, custom typeface | 288 |
| `renault` | Aurora gradients, French design, zero-radius buttons | 311 |
| `tesla` | Radical subtraction, cinematic photography, minimal UI | 286 |

### Other

| Product | Style Keywords | Lines |
|---------|---------------|-------|
| `uber` | Black/white, mobility platform, map-centric, clean | 295 |
| `spotify` | Green accent, music streaming, dark mode, audio-first | 246 |
| `airbnb` | Warm coral, travel marketplace, belonging aesthetic | 246 |

## Tips

1. **Combine styles**: Read multiple DESIGN.md files to create hybrid designs
2. **Focus on tokens**: The color hex values and typography specs are the most actionable parts
3. **Agent Prompt Guide**: Each DESIGN.md ends with ready-to-use prompts — use them directly
4. **Shadow systems**: Many files have unique shadow approaches (Vercel's shadow-as-border, Linear's layered elevation)
5. **Typography is key**: Font choice and letter-spacing often define the entire feel

## Source

Based on [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md), MIT License.
