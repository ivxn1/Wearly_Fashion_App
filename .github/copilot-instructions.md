# Wearly — Copilot Instructions (SoftUni Django Basics Exam)

## Project context
This repository is a Django + PostgreSQL web app called "Wearly" (fashion planning assistant).
Core apps:
- core: base layout, home page, errors (404), site-level pages (about/contact)
- wardrobe: garments catalog (filters, sort, pagination), garment CRUD
- outfits: outfits CRUD + relations to garments
- planner: plans/schedule entries referencing outfits

UI style: monochrome “premium liquid glass” aesthetic (blur, subtle borders, inset highlights), consistent spacing, reusable cards and sections. Bootstrap may be present, but custom CSS defines the final look.

## Exam/originality constraints (VERY IMPORTANT)
- Do NOT generate large blocks of code end-to-end.
- Prefer explanations + small focused snippets (5–25 lines) over full files.
- When the user asks for full implementation, respond with step-by-step guidance and minimal examples, so the user writes the majority.
- Avoid creating entire apps, full CRUD flows, or multiple-file dumps in one response.
- Always favor teaching: explain what each part does and why.

## Coding standards
- Use Django best practices and clean code: small functions, cohesive modules, clear naming.
- Keep business logic in views/services (if used), keep templates mostly presentation.
- Prefer deterministic, readable querysets (avoid clever one-liners).
- Use select_related/prefetch_related appropriately for FK/M2M to avoid N+1 queries.
- Always preserve query parameters for pagination links on filtered list views.
- Use redirects after successful POST; validate on both model/form where appropriate.
- Add user-friendly error messages, labels, placeholders, and help texts.

## Frontend standards
- Keep shared component styles in reusable CSS (e.g., cards/buttons/forms) and page-specific tweaks in page CSS.
- Cards must have stable layout (bottom row aligned using flex patterns).
- Ensure responsive behavior: grids collapse nicely, filter form stacks on mobile, navbar works on small screens.
- Avoid inline styles unless absolutely necessary.

## Templates
- Use base template + inheritance.
- Use reusable partial templates and/or custom inclusion tags for repeated sections/cards.
- Provide friendly empty states (headers stay, message + CTA when empty).

## Data & environment
- PostgreSQL for DB.
- Do not commit secrets/credentials. Use .env for local secrets.
- Media uploads exist; do not commit uploaded media. Use README to explain media setup and provide optional sample images in static if needed.

## Output format preference
- When asked for code: provide minimal patches and explain where to place them.
- When asked for architecture: provide a checklist or step-by-step plan.
- When uncertain about project conventions, ask to reference existing names (URL names, template paths) instead of inventing new ones.