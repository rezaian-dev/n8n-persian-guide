# Contributing

Report technical corrections with the chapter, n8n version, expected result, and a reproducible example using synthetic data. Do not upload tokens, credentials, customer payloads, or workflow exports containing private pinned data.

## Sources of truth

- `guide.md`: Persian article text.
- `scripts/book-notes.json`: chapter objectives and review exercises.
- `scripts/book.css` and `scripts/build_pdf.py`: PDF layout and publication.
- `scripts/landing.html`, `docs/assets/landing.css`, and `docs/assets/landing.js`: website.
- `scripts/build_figures.py`: original technical illustrations.

Do not directly edit generated HTML, PDF, metadata, or PDF previews. Regenerate them and include them with the corresponding source changes.

```bash
python -m pip install -r requirements.txt
npm test
python scripts/build_pdf.py
python scripts/build.py
python scripts/check.py
python scripts/check_pdf.py
```

Consult the root README for system requirements and optional illustration tooling. Keep changes focused, cite official sources for version-sensitive claims, preserve reduced-motion behavior, and state what was actually tested. Never label an example production-ready without evidence.
