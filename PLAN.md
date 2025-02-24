# Percy Web Interface Implementation Plan

## Architecture Overview
- **Framework**: Next.js 14 (App Router) with Static Exports (`next export`)
- **UI Components**: Shadcn UI + Radix Primitives + Tailwind CSS
- **Data Strategy**: Client-side data fetching with SWR + zod for schema validation
- **Hosting**: Cloudflare Pages (static deployment)

## Directory Structure
```
web/
├── app/                 # Next.js app router
│   ├── (static)/        # Static generated pages
│   │   ├── handbook/    
│   │   └── models/     
│   ├── about/page.tsx   
│   └── layout.tsx
├── components/          # Shadcn + custom components
├── data/                # Symlink to project data files
├── lib/                 # Data loading utilities
├── styles/              # Tailwind config + custom CSS
└── next.config.js       # Static export config
```

## Implementation Phases

### 1. Project Setup (Week 1)
- Initialize Next.js with `create-next-app` in `/web`
- Configure `next.config.js` for static exports
- Set up Shadcn UI with theming support
- Create symlink from `/web/data` to project root data files
- Add data types from JSON schemas using `zod`

### 2. Homepage & Core Layout (Week 2)
- Hero section with project overview
- Key metrics cards (total tests run, top models)
- Interactive model comparison chart (visx)
- Responsive navbar with search
- Footer with project links

### 3. Handbook System (Week 3)
- Markdown processing pipeline:
  - Convert handbook markdown to AST (remark)
  - Generate static pages under `/handbook/[chapter]`
  - Table of Contents component with collapsible sections
- Search integration with Fuse.js
- Diagram rendering for question images

### 4. LLM Leaderboard (Week 4)
- TanStack Table implementation with:
  - Dynamic column visibility
  - Column filtering (react-hook-form)
  - Server-style pagination
- Metrics cards summary
- CSV export functionality
- Score distribution histogram

### 5. Model & Test Pages (Week 5)
- Dynamic routes:
  - `/models/[modelId]` - Model capability matrix
  - `/providers/[providerId]` - Cost/performance charts
  - `/tests/[testId]` - Question-by-question analysis
- Test result viewer components:
  - Diff viewer for model vs correct answers
  - Token usage waterfall charts
  - RAG context inspector

## Performance Optimization
- Data caching strategy:
  - Client-side cache with SWR (stale-while-revalidate)
  - Compress JSON data with lz-string
  - Preload critical pages with `<link rel="preload">`
- Image optimization:
  - Convert diagrams to WebP
  - Implement blur-up placeholders

## Deployment Setup
```bash
# Cloudflare Pages config (web/cloudflare.json)
{
  "build": {
    "command": "npm run export",
    "directory": "out"
  }
}
```

## Post-Launch
- Add Vercel Analytics for usage tracking
- Implement automated accessibility testing
- Create feedback widget for data quality reports
- Set up CI checks for data schema validation
