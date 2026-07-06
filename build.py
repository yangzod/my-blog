#!/usr/bin/env python3
"""Render markdown posts to static HTML under docs/."""
import shutil
from pathlib import Path

import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader

import config

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
OUTPUT_DIR = ROOT / "docs"
ASSETS_DIR = OUTPUT_DIR / "assets"


def parse_post(path: Path) -> dict:
    post = frontmatter.load(path)
    md = markdown.Markdown(extensions=["fenced_code", "tables", "toc"])
    html = md.convert(post.content)
    # Strip the leading YYYY-MM-DD- prefix from the filename for the slug.
    slug = path.stem[11:] if len(path.stem) > 11 and path.stem[10] == "-" else path.stem
    date = post["date"]
    # Site-relative URL (no leading slash) so it composes with the page's rel prefix.
    url = date.strftime(f"%Y/%m/%d/{slug}/")
    return {
        "title": post["title"],
        "date": date,
        "excerpt": post.get("excerpt", ""),
        "content": html,
        "url": url,
    }


def main() -> None:
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=False)

    post_paths = sorted(POSTS_DIR.glob("*.md"), reverse=True)
    posts = [parse_post(p) for p in post_paths]

    # Clean output directory so deleted posts don't linger.
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Render each post page.
    post_tmpl = env.get_template("post.html")
    for post in posts:
        out_dir = OUTPUT_DIR / post["url"]
        out_dir.mkdir(parents=True, exist_ok=True)
        # One "../" per path segment; post.url like "2026/07/01/slug/" has 4 slashes = 4 levels deep.
        rel = "../" * post["url"].count("/")
        (out_dir / "index.html").write_text(
            post_tmpl.render(post=post, site=config.SITE, rel=rel),
            encoding="utf-8",
        )

    # Render homepage with recent posts.
    index_tmpl = env.get_template("index.html")
    recent = posts[: config.SITE["recent_count"]]
    (OUTPUT_DIR / "index.html").write_text(
        index_tmpl.render(posts=recent, site=config.SITE, rel=""),
        encoding="utf-8",
    )

    # Copy static assets.
    shutil.copytree(STATIC_DIR, ASSETS_DIR)

    print(f"Built {len(posts)} posts into {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
