<div align="center">

<img src="docs/assets/social.png" alt="n8n Persian Guide — a practical, illustrated engineering handbook" width="100%" />

# n8n Persian Guide

### From connected tools to reliable systems

**Written and curated by Mohammadreza Rezaian**

[**Download the PDF**](docs/N8N-Persian-Guide.pdf) · [**Explore the book website**](https://rezaian-dev.github.io/n8n-persian-guide/) · [**Read the source**](guide.md)

**35 designed A4 pages · 26 chapters · 6 original technical illustrations · 10 independent tests**

</div>

## What this repository contains

A practical Persian-language guide to n8n: data and expressions, webhooks, API integration, input validation, idempotency, error handling, deployment, security, observability, recovery, and controlled AI workflows.

The **PDF is the primary deliverable**. Its editorial layout is inspired by the author's [TypeScript Persian Guide](https://github.com/rezaian-dev/typescript-persian-guide): independent chapter openings, learning objectives, navy-and-gold accents, syntax-highlighted code frames, exercises, acceptance checks, clickable contents, and PDF bookmarks.

The website is a **book introduction and download page**, not a duplicate full-text reader. It features real PDF previews, chapter-to-PDF links, a responsive book presentation, and locally bundled **Motion 14.9.0** animations. Reduced-motion preferences are respected. No CDN, analytics, tracking, or runtime framework is required.

**Documentation reviewed:** November 1, 2026. **Example baseline:** n8n 2.45.7. These are dated references, not a claim that this version will always be current.

## Read, then build

| Track | Topics |
| --- | --- |
| Foundations | Events, nodes, items, expressions, tool selection, licensing |
| First workflow | Local setup, webhooks, validation, HTTP responses, APIs |
| Reliability | Durable intake, duplicate handling, retries, compensation |
| Operations | PostgreSQL, external runners, TLS, security, queue mode, recovery |
| Controlled AI | Structured output, RAG, tool permissions, human approval |
| Verification | Evaluation, troubleshooting, release checks, learning roadmap |

The PDF adds chapter objectives and practical review exercises to the Markdown article. These editorial notes are maintained in `scripts/book-notes.json`.

## Try the local example

Requires Docker with Compose. Use **synthetic data only**.

```bash
git clone https://github.com/rezaian-dev/n8n-persian-guide.git
cd n8n-persian-guide
docker compose -f deploy/compose.local.yaml up -d
```

Open `http://localhost:5678`, create a local owner account, and import [`workflows/lead-intake.json`](workflows/lead-intake.json). Follow chapter 7 of the PDF.

The demonstration validates a lead and returns HTTP `200` or `422`. It **does not persist submissions, contact a CRM, or send messages**. Its unauthenticated webhook is intended only for isolated local testing. Do not expose it publicly without authentication, rate limiting, and an appropriate security review.

The server Compose file is a **staging starting point**, not a complete production deployment. Replace every secret in `deploy/.env.example`, keep n8n and runner versions aligned, configure HTTPS through a host reverse proxy, and test recovery. Never use `down -v` on data you need to retain.

## Build and validate

Requires Python 3.10+, Node.js 20+, and the system libraries required by WeasyPrint, including Pango, HarfBuzz, Fontconfig, and DejaVu Sans Mono. See the [WeasyPrint installation guide](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation) for OS-specific setup.

```bash
python -m pip install -r requirements.txt
npm test
python scripts/build_pdf.py
python scripts/build.py
python scripts/check.py
python scripts/check_pdf.py
python -m http.server 8080 --directory docs
```

The PDF builder also renders the real cover and sample-page previews. Committed metadata supplies the website's page count, download size, and exact PDF chapter links. Source and layout hashes detect a stale PDF.

To regenerate the original illustrations, install the optional artwork tooling:

```bash
python -m pip install playwright==1.64.1
python -m playwright install --with-deps chromium
python scripts/build_figures.py
python scripts/build_pdf.py
python scripts/build.py
```

The distributed images are already included; normal reading, website hosting, and CI do not require Playwright.

## Verification and limitations

- **10 independent Node.js tests** cover validation logic, item linkage, and workflow structure.
- PDF checks cover source/layout freshness, page metadata, searchable text, bookmarks, internal destinations, and text outside page bounds.
- Website checks validate local assets and links. Desktop/mobile checks also exercised theme switching, contents expansion, and PDF downloads.
- Motion effects were checked with normal and reduced-motion preferences. Motion and its MIT license are stored locally under `docs/assets/vendor/`.
- PDF covers, representative pages, and a thumbnail overview were visually reviewed. This is not a complete human copyedit or a PDF/UA accessibility certification.
- Full workflow import/execution inside n8n, Docker startup, external services, TLS, and backup restoration still require testing in the target environment. AI sections are implementation designs, not live connected agents.

## Repository layout

```text
.
├── guide.md                       # Persian article source
├── docs/
│   ├── N8N-Persian-Guide.pdf       # Primary publication
│   ├── index.html                 # Generated book landing page
│   ├── assets/                    # Local font, author photo, Motion, site assets
│   ├── figures/                   # Six original technical illustrations
│   └── previews/                  # Images rendered from the actual PDF
├── workflows/lead-intake.json      # Importable local demonstration
├── examples/normalize-lead.js      # Dependency-free validation logic
├── tests/                         # Independent example tests
├── deploy/                        # Local/staging Compose and proxy example
└── scripts/                       # Publication sources, builders, and checks
```

There is one distributed PDF and no duplicate HTML reader, duplicate deployment documentation, dependency directories, private environment files, or test screenshots in the repository. The generated website and publication assets are retained because GitHub Pages serves them directly.

## Publishing

GitHub Pages uses the `main` branch and `/docs` directory. Commit regenerated publication files together. Pages serves the book website; it does **not** host n8n itself.

## Author and rights

**Mohammadreza Rezaian — Front-End Engineer**<br />
[Portfolio](https://rezaian-dev.vercel.app/fa) · [GitHub](https://github.com/rezaian-dev) · [Email](mailto:mrezaian.dev@gmail.com)

Prepared with AI-assisted research and writing. Sources, review date, and verification limits are documented. Corrections are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md). Never publish credentials or customer data in an issue.

Text, design, examples, and the author's photograph: all rights reserved; see [LICENSE.md](LICENSE.md). Motion is MIT-licensed and Vazirmatn uses SIL OFL; their original licenses are included. n8n has its own Sustainable Use / Enterprise licensing. This is an independent guide, not an official n8n publication.
