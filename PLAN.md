# Percy Web Interface Development Plan

## Phase 1: Project Setup & Core Infrastructure
- [ ] Initialize Next.js 14 app with App Router in `/web`
- [ ] Configure for static export (`output: 'export'`)
- [ ] Set up Shadcn UI components library
- [ ] Add TanStack Table + react-hook-form integration
- [ ] Create TypeScript types from JSON schemas using `json-schema-to-typescript`

## Phase 2: Core Pages & Features
### Homepage (/) 
- Hero section explaining project goals
- License class overview cards
- Quick stats from board.json

### Handbook Browser (/handbook)
- first, remember that we are using nextjs to export static pages for the table of contents and each group.
- Dynamic routing for groups (/handbook/[group])
- Markdown content rendering, we have no need for syntax highlighting
- navigate via shadcn Select component with chapter and group titles
- the table of contents is available in web/src/handbook/toc.json
- the url path /handbook/ shows the table of contents with links
- the individual group markdown files are in web/src/handbook/md, like web/src/handbook/md/T1A.md. the title of the group is located in this markdown file as the first line.

### LLM Leaderboard (/leaderboard)
- Filterable/sortable table of board.json data
- Provider/Model comparison charts
- Dynamic filtering by:
  - License class
  - Model capabilities
  - Cost ranges
  - Performance metrics

### Model & Test Exploration
- Model detail pages (/models/[id]) with:
  - Capability matrix from llmstats.json
  - Cost calculator
  - Historical performance
- Test result pages (/tests/[id]) showing:
  - Question-by-question results
  - RAG context visualization
  - Token usage breakdowns
  - Original prompts/responses

## Phase 3: Data Loading & Optimization
- Implement client-side data loading strategy:
  - Prebuild JSON files to `/web/public/data`
  - SWR for client-side caching/revalidation
  - Compression with JSONC format
- Generate TypeScript types from schemas:
  - Board data
  - LLM stats
  - Test results
- Optimize static assets:
  - Convert handbook images to WebP
  - Lazy load question diagrams

## Phase 4: Deployment Setup
- Configure next.config.js for static export
- Add CI/CD pipeline:
  - Rebuild JSON data files on schema changes
  - Regenerate TypeScript types
  - Preprocess handbook markdown
- Cloudflare Pages deployment setup
- Edge caching headers for JSON data

## Phase 5: Interactive Features
- Compare mode for model performance
- Model "shootout" test generator
- Interactive cost estimator
- User-submitted test results (CSV import)

Ownership:
- Web Team (Frontend Engineers x2)
- Data Team (Backend Engineer x1)
- DevOps (Cloudflare Config)
