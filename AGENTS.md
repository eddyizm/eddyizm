# eddyizm.com — Django Blog Project

## Repo layout

- `main/` — Django project root (settings, urls, views, wsgi, manage.py, gunicorn.conf.py)
- `main/blog/` — Blog app (models, views, urls, templates, tests, ffe_utils.py)
- `main/main/` — Django app package (settings.py, urls.py, views.py, wsgi.py, apps.py — if exists)
- `main/static/` — Static files (CSS, JS, images)
- `main/media/` — User-uploaded media
- `main/data/` — Logs (access.log, error.log), DB (db.sqlite3), and other runtime data
- `main/blog/migrations/` — Database migrations for the blog app
- `main/.env` — Development env (DEBUG=debug, dev DB path)
- `main/.prod.env` — Production env (DEBUG=prod, prod DB path)
- `main/Caddyfile` — Reverse proxy / TLS config for eddyizm.com
- `main/requirements.txt` — Python dependencies

## Key commands

### Dev server
```bash
# Activate virtual environment first
source env/bin/activate
# Run Django development server (uses SQLite)
python manage.py runserver
# Run a single test
python manage.py test blog.tests
# Run all tests
python manage.py test
# Run a specific test case class
python manage.py test blog.tests.BlogPostTests
```

### Production / container
```bash
# Build the podman image
podman build -t eddyizm_blog -f ContainerFile --ignorefile .dockerignore
# Run the container
podman run --name=blog -d -p 8000:8000 -v ~/src/eddyizm/data:/data:rw -v ~/src/eddyizm/static:/static:rw -v ~/src/eddyizm/media:/media:rw localhost/eddyizm_blog
# Run with gunicorn directly (no container)
gunicorn -c main/gunicorn.conf.py main.wsgi:application
```

### Caddy (reverse proxy)
```bash
# Start Caddy in dev mode (debug)
caddy run
# Start Caddy in prod mode
caddy run --config Caddyfile
```

## Environment

- The project loads `.env` at `main/settings.py` via `load_dotenv()`
- `DEBUG` is set from `.env` (default: `debug` → `True`) vs `.prod.env` (`prod` → `False`)
- Key env vars: `SECRET_KEY`, `MAILGUN_KEY`, `FFE_KEY`, `TURNSTILE_SITEKEY`, `TURNSTILE_SECRET`, `ADMIN_URL`, `DB_PATH`, `DB_FILE`, `STATIC_ROOT`, `MEDIA_ROOT`
- `.env` is a developer-only file — do not commit it; it's in `.gitignore`
- Use `env/bin/activate` to activate the Python virtual environment

## Django specifics

- Database: SQLite3 (path from `DB_PATH` + `DB_FILE` env vars)
- Cache: `TTLCache` with `maxsize=128`, `ttl=60 * 60 * 2` (2 hours) on blog views
- Security: `django-bleach` (allowed tags: `p`, `a`, `br`, `code`, `pre`, `img`, `blockquote`, `q`), `django-turnstile` (CAPTCHA), `django-honeypot`
- The `blog/` app has a custom `post_detail` view with cache; `blog_posts` and `blog_category` use `TTLCache` too
- `blog/views.py` imports from `blog.ffe_utils` (sub-module of the blog app)
- `manage.py` and `wsgi.py` both set `DJANGO_SETTINGS_MODULE=main.settings`

## Caddy configuration

- The `Caddyfile` is at `main/Caddyfile`
- Domain: `eddyizm.com` with TLS; `www.eddyizm.com` redirects to main domain
- Static files served from `/home/eddyizm/static/`
- Media files served from `/home/eddyizm/media/`
- `import cors` for CORS headers

## Testing

- Tests live in `main/blog/tests.py`
- Run with `python manage.py test` (uses the Django test runner)
- Tests use Django's test database (auto-created, auto-dropped)
- `BlogPostTests` uses a real DB with `setUp` creating author, category, and a blog post
- `SimpleTestCase` subclasses (no DB) are for URL and view logic without database
- The blog has a cache-based `post_detail` view; cache keys are the post `id`
- `blog/ffe_utils.py` functions are used by blog views (get_FFE, get_daily_q, get_random_q, send_message)

## Important notes

- The `main/main/` directory contains the Django app package (settings.py, urls.py, views.py, wsgi.py)
- The `main/blog/` directory is a separate Django app within the same project
- `manage.py` sets `DJANGO_SETTINGS_MODULE=main.settings` to find the right settings module
- The `main/` project root is NOT the `main/` package — `manage.py` uses `main.settings` (i.e., `main/main/settings.py` is the settings module)
- The `main/gunicorn.conf.py` is at `main/main/gunicorn.conf.py`, not at `main/gunicorn.conf.py`
- The `main/.env` has `DEBUG=debug` — the `.prod.env` has `DEBUG=prod`
- The `main/data/` directory contains `db.sqlite3`, `access.log`, `error.log`, `quotes_app.sqlite3`
- The `main/static/blog/assets/` directory has `css/`, `js/`, `sass/` subdirectories

## Build & lint

- `pip install -r requirements.txt` (from the virtual environment)
- `python manage.py migrate` (apply DB migrations)
- `python manage.py check` (run system checks)
- No explicit linting in the repo (`.vscode/settings.json` has linting disabled)
- Run `python -m pytest` if pytest is used (no pytest config found)

## Monorepo / multi-package

This is a single Django project with a `main/` app and a `blog/` app. There is no separate library package. The `main/` directory is both the Django project root and the app package.

## graphify

This project has a knowledge graph at `graphify-out/` with god nodes, community structure, and cross-file relationships.

### Build the graph
```bash
graphify extract .
graphify cluster-only .          # generate GRAPH_REPORT.md + graph.json
graphify update .                # after any code change, keeps graph current
```

### How to query
- `graphify query "<question>"` — broad search (default when graph.json exists)
- `graphify path "<A>" "<B>"` — relationship between two nodes
- `graphify explain "<concept>"` — focused concept lookup
- Results are scoped to a subgraph, typically small.

### Known findings (from `graphify cluster-only .`)
- **143 nodes, 189 edges, 14 communities** (4 thin communities omitted)
- **God nodes**: `BlogPost` (13 edges), `Category` (11 edges), `BlogPostTests` (8 edges), `MusicTrack` (5 edges), `Author` (5 edges), `t()` (4 edges), `ContactForm` (3 edges), `AboutpageTests` (3 edges), `BlogHomePageTests` (3 edges), `ProjectsCFCTests` (3 edges)
- **Key connections**: `blog_category()` → `BlogPost` (views → models); `BlogPostTests` → `Author`, `BlogPost`, `Category` (tests → models)
- **No import cycles** detected
- **Extract rate**: 93% EXTRACTED, 7% INFERRED, 0% AMBIGUOUS

### When to skip graphify
- Only skip if the task is about stale or incorrect graph output
- Do not skip for routine codebase questions

### Read `graphify-out/GRAPH_REPORT.md` for broad architecture review
- Use `graphify path` or `graphify explain` for focused queries when the report isn't enough

### After modifying code
Always run `graphify update .` (AST-only, no API cost) to keep the graph current.

### Additional graphify commands
```bash
# List all communities
graphify cluster-only .

# Get node details
graphify query "BlogPost"

# Get relationships between two nodes
graphify path "BlogPost" "Category"

# Get the most connected nodes
graphify god-nodes .
```
