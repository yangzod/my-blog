# my-blog

A simple static blog generator for GitHub Pages.

## Usage

```bash
pip install -r requirements.txt
python build.py
```

The build output (`index.html`, `YYYY/MM/DD/slug/index.html`, `assets/`) is written directly to the project root. Commit it alongside the source so GitHub Pages can serve it.

## Structure

- `posts/` — markdown source files, named `YYYY-MM-DD-slug.md`
- `templates/` — Jinja2 templates
- `static/` — source assets, copied to `assets/` on build
- `build.py` — render script
- `config.py` — site metadata
