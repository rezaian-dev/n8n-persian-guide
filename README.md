<div align="center">

<img src="docs/assets/social.png" alt="n8n Persian Guide — an illustrated engineering reference" width="100%" />

# n8n Persian Guide

**Written and curated by Mohammadreza Rezaian**

[**Download PDF**](docs/N8N-Persian-Guide.pdf) · [**Book website**](https://rezaian-dev.github.io/n8n-persian-guide/) · [**Persian source**](guide.md)

**71 A4 pages · 26 chapters · 76 answered interview questions · 3 projects/labs · 34 independent tests**

</div>

A project-based Persian reference to reliable automation: n8n data and expressions, webhooks, APIs, validation, idempotency, error handling, deployment, security, recovery, RAG and controlled AI tools.

The **PDF is the primary publication**. The website introduces the book and provides downloads, real PDF previews and chapter links; it is not a duplicate full-text reader. The flat cover keeps conceptual artwork, searchable lettering and the original portrait separate. The PDF includes vector icons, exercises, dotted contents and bookmarks. The website uses local Motion animations and supports 320px layouts, keyboard interaction and reduced motion.

**Sources reviewed:** November 1, 2026. **Example baseline:** n8n 2.45.7. These dated references are not a guarantee of the latest version.

## Repository structure

| Location | Purpose |
| --- | --- |
| `guide.md` | Persian text and official references |
| `docs/` | Distributed PDF and GitHub Pages website, with required local assets |
| `scripts/` | Editable publication sources, builders and one validation entry point |
| `workflows/` | Importable local n8n example |
| `examples/` | Code-node source checked against the workflow export |
| `projects/` | Independent durable-intake and AI-boundary learning labs |
| `tests/` | 22 Node.js and 12 Python tests |
| `deploy/` | Local/staging Compose and reverse-proxy examples |

Generated publication files are committed because Pages serves `main:/docs`. Their editable sources are also necessary for reproducible updates. There are no dependency folders, private environment files, scratch screenshots or duplicate HTML readers in Git. Font and Motion licenses must remain with their bundled assets.

## Run the local n8n example

Requires Docker with Compose. Use synthetic data only.

```bash
docker compose -f deploy/compose.local.yaml up -d
```

Open `http://localhost:5678`, create a local owner account and import [`workflows/lead-intake.json`](workflows/lead-intake.json). Follow chapter 7.

The example returns `200` or `422` after validation. It **does not persist submissions, contact a CRM or send messages**. The unauthenticated webhook is only for isolated local testing. Public exposure requires authentication, rate limiting and a security review.

The server Compose file is a **staging starting point**, not a production deployment. Replace secrets in `deploy/.env.example`, align n8n/runner versions, configure TLS and test recovery. Never use `down -v` on data you need.

## Independent learning labs

| Lab | Run | Boundary |
| --- | --- | --- |
| [Durable intake / outbox](projects/durable_intake.py) | `python -m unittest discover -s tests -p 'test_*.py' -v` | Atomic local receipt/intent, duplicate conflict, lease ownership and restart persistence |
| [AI trust boundaries](projects/ai_boundary.mjs) | `node --test tests/ai_boundary.test.mjs` | Strict output schema, tenant/group document eligibility, scoped tools and matching approval |

Worked experiments are included in chapters 10 and 19. These labs have **no live n8n, model, vector database, MCP server or external-tool connection**.

- **Outbox:** delivery is at-least-once. A crash after external success but before acknowledgement can repeat an effect. Downstream idempotency or reconciliation remains necessary. SQLite is a teaching tool, not n8n Queue mode configuration. `source` must come from authenticated context; serialization is Python-local, not an interoperable signing standard. Automatic attempt caps, dead-letter handling, retention, monitoring and production hardening are not implemented. Exercise: add a maximum-attempt policy, inspectable terminal state and authorized replay tests.
- **AI:** context and approvals must come from trusted authentication and audit systems. A digest is not a signature or identity proof. The pure approval check does not atomically consume an approval or guarantee one-time execution. Exercise: add an authenticated approval store and test concurrent consumption, expiry and crashes after delivery.

## Build and validate

Requires **Python 3.10+**, **Node.js 20+**, and WeasyPrint system libraries including Pango, HarfBuzz, Fontconfig and DejaVu Sans Mono. See [WeasyPrint installation](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation). No Node package installation or package manifest is needed: tests use the built-in runner.

```bash
python -m pip install -r requirements.txt
node --test tests/*.test.mjs
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/build_pdf.py
python scripts/build.py
python scripts/check.py
python -m http.server 8080 --directory docs
```

Edit `guide.md`, `scripts/book-notes.json` and `scripts/book.css` for the book; edit `scripts/landing.html` and `docs/assets/landing.{css,js}` for the website. Regenerate the PDF, previews, metadata and landing page together. Do not hand-edit generated publication content.

Optional illustration regeneration requires Playwright, not normal reading, hosting or CI:

```bash
python -m pip install playwright==1.64.1
python -m playwright install --with-deps chromium
python scripts/build_figures.py
python scripts/build_pdf.py
python scripts/build.py
```

## Verification and limits

The 34 independent tests cover example logic and policy boundaries, **not** full n8n execution or production readiness. The unified checker validates local assets, links, PDF source/layout freshness, bookmarks, destinations, searchable text and page bounds. Typesetting also checks all 130 learning-icon placements for slot containment, centering and text-box overlap. Representative PDF pages were visually reviewed; this is not PDF/UA certification or a complete human copyedit.

Docker startup, workflow import/runtime, TLS, external services, capacity and backup restoration require tests in the target environment. Learning requires running experiments and explaining failure modes, not just reading.

`.gitattributes` limits GitHub language statistics to the reader-facing HTML, CSS and JavaScript. Python tooling/labs and other auxiliary code remain usable but are excluded; bundled Motion is vendored. GitHub may cache its statistics after a push.

## Corrections and security

For a correction, include the chapter, software version, expected result and a minimal synthetic example. Keep changes focused, cite official sources and state the actual test scope. Never publish credentials, customer data, private pinned payloads or unsanitized workflow exports.

Report vulnerabilities in these examples or the website privately to **mrezaian.dev@gmail.com**. Report n8n product vulnerabilities through its upstream security process. This repository does not run a public n8n service.

## Author and rights

**Mohammadreza Rezaian — Front-End Engineer** · [Portfolio](https://rezaian-dev.vercel.app/fa) · [GitHub](https://github.com/rezaian-dev)

Prepared with AI-assisted research and writing. Text, design, examples and portrait: all rights reserved; see [LICENSE.md](LICENSE.md). Motion is MIT-licensed and Vazirmatn uses SIL OFL; their original licenses are bundled. n8n has separate Sustainable Use / Enterprise licensing. This is an independent guide, not an official or endorsed n8n publication.
