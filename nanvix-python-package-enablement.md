# Nanvix Python Distribution

This document details the execution plan for the Nanvix Python distribution. The scope is to enable
80 Python packages/libraries presented in the [Package Index](#5-python-package-index). Overall, these are grouped into
six active categories (A–F) spanning three technical layers:

- **Python stdlib modules** — 14 modules (Category A), mostly already included
- **Pure Python packages** — 56 packages (Categories B, E, F), no native code required
- **Native C/C++ extension packages** — 10 packages (Categories C, D), require cross-compilation

---

## 1. Package Classification

| Category | Count | Effort | Examples | Prerequisites |
| -------- | ----: | ---------- | -------- | ------- |
| **A - Python stdlib** | 14 | None (already supported) | os, json, csv, re, datetime, pathlib | None |
| **B - Pure Python** | 47 | Low (copy into ramfs) | tqdm, chardet, Jinja2, click, tabulate, PyPDF2, pydantic | Package infra |
| **C - C extensions (self-contained)** | 5 | Medium (cross-compile) | numpy, lxml, psutil, cryptography, rapidfuzz | Cross-compilation tooling + `dlopen` / dynamic loading |
| **D - C extensions (heavy deps)** | 5 | High (port dependencies) | pandas, Pillow, matplotlib, scipy, wordcloud | Category C packages + native libs + dynamic loading |
| **E - Subprocess-dependent** | 4 | Very High (OS work) | moviepy, pydub, ffmpeg-python, pytesseract | fork/exec — process management + native tools |
| **F - Networking-dependent** | 5 | Very High (OS work) | requests, httpx, feedparser | Socket support — TCP/IP networking |
| **G - Deferred** | 15 | TBD | scikit-learn, spacy, opencv-python, polars, duckdb | Evaluate after Categories C–F; see [§3](#3-deferred) |
| **H - Out of scope** | 4 | N/A | pandoc, playwright, pyautogui, wmi | Fundamentally incompatible; see [§4](#4-out-of-scope) |

---

## 2. Execution Plan

| Week | Category | New Packages Enabled | Cumulative Pkgs |
| ---- | -------- | -------------------- | --------------: |
| 1 | A | Harden stdlib support | 14 |
| 2 | B | 20 pure Python packages | 20 |
| 3 | B | 23 pure Python packages (documents, creative content, reference) | 43 |
| 5 | C, D | Cross-compilation infra + native libs | 43 |
| 6 | C | numpy | 44 |
| 7 | D | pandas, scipy | 46 |
| 8 | C, D | Pillow, lxml | 48 |
| 9 | B, D | matplotlib, seaborn | 50 |
| 10 | B, C, D | psutil, cryptography, rapidfuzz, wordcloud, sympy, plotnine, altair | 57 |
| 15 | E | moviepy, pydub, ffmpeg-python, pytesseract | 61 |
| 18 | F | requests, urllib3, httpx, feedparser, pyperclip | 66 |

---

## 3. Deferred

Viable once prerequisites land; evaluate after the category noted.

| Item | Reason | Evaluate After |
| ---- | ------ | -------------- |
| opencv-python | Enormous C++ codebase | Category D (C extensions) |
| spacy / nltk / gensim | Large NLP frameworks — heavy dependencies | Category D (C extensions) |
| scikit-learn / statsmodels | Large ML/stats frameworks — heavy C/Fortran deps | Category D (C extensions) |
| duckdb | In-process SQL — large C++ build | Category D (C extensions) |
| polars | Rust-backed DataFrames — requires Rust cross-compilation | Category D (C extensions) |
| h5py | HDF5 files — requires libhdf5 port; lower priority | Category D (C extensions) |
| librosa | Audio analysis — heavy C deps (libsndfile, numba) | Category D (C extensions) |
| PyMuPDF (fitz) | Fast PDF — large C dependency (MuPDF) | Category D (C extensions) |
| Cloud SDKs (boto3, google-api-python-client) | Need networking first; lower priority | Category F (networking) |
| scrapy, celery, APScheduler | Complex frameworks; need networking + multiprocessing | Category F (networking) |
| fastapi / uvicorn / hypercorn | Web server framework — needs networking + async event loop | Category F (networking) |
| aiohttp / websockets | Async networking — needs sockets + full async support | Category F (networking) |
| tweepy / praw | Social media APIs — needs networking; niche use case | Category F (networking) |
| slack-sdk | Slack API — needs networking | Category F (networking) |
| paramiko / fabric | SSH — needs cryptography + sockets | Category F (networking) |

---

## 4. Out of Scope

Fundamentally incompatible with the Nanvix target (no browser, no display server, wrong OS).

| Item | Reason |
| ---- | ------ |
| pandoc | Haskell runtime; no viable cross-compilation path |
| playwright / selenium | Browser automation — no browser on Nanvix |
| GUI tools (pyautogui) | No display server |
| wmi / pywin32 | Windows-only — N/A for Nanvix (i686-linux target) |

---

## 5. Python Package Index

| Package | Type | Category | Prerequisites |
| ------- | ---- | ---- | ------- |
| os | Stdlib | A | None |
| pathlib | Stdlib | A | None |
| shutil | Stdlib | A | None |
| glob | Stdlib | A | None |
| json | Stdlib | A | None |
| csv | Stdlib | A | None |
| tempfile | Stdlib | A | None |
| platform | Stdlib | A | None |
| re | Stdlib | A | None |
| datetime | Stdlib | A | None |
| email | Stdlib | A | Partial (parsing works, send needs sockets) |
| smtplib | Stdlib | A | TCP/IP sockets |
| imaplib | Stdlib | A | TCP/IP sockets |
| subprocess | Stdlib | A | fork/exec |
| tqdm | Pure Python | B | None |
| chardet | Pure Python | B | None |
| python-dotenv | Pure Python | B | None |
| click | Pure Python | B | None |
| typer | Pure Python | B | None |
| tenacity | Pure Python | B | None |
| pydantic | Pure Python | B | None (pure Python mode) |
| Jinja2 | Pure Python | B | None (pure Python fallback) |
| markupsafe | Pure Python | B | None (pure Python fallback) |
| pytest | Pure Python | B | None |
| pluggy | Pure Python | B | None |
| iniconfig | Pure Python | B | None |
| packaging | Pure Python | B | None |
| tabulate | Pure Python | B | None |
| coverage | Pure Python | B | None |
| pytest-cov | Pure Python | B | None |
| hypothesis | Pure Python | B | None |
| loguru | Pure Python | B | None |
| pygments | Pure Python | B | None |
| typing-extensions | Pure Python | B | None |
| PyPDF2 / pypdf | Pure Python | B | None |
| pdfplumber | Pure Python | B | None |
| python-docx | Pure Python | B | None |
| python-pptx | Pure Python | B | None |
| openpyxl | Pure Python | B | None |
| reportlab | Pure Python | B | None (mostly pure; some C) |
| beautifulsoup4 | Pure Python | B | None (html.parser mode) |
| pyyaml | Pure Python | B | None (pure Python fallback) |
| markdownit-py | Pure Python | B | None |
| markdownify | Pure Python | B | None |
| fpdf2 | Pure Python | B | None |
| docx2txt | Pure Python | B | None |
| Faker | Pure Python | B | None |
| qrcode | Pure Python | B | None |
| svgwrite | Pure Python | B | None |
| networkx | Pure Python | B | None |
| srt | Pure Python | B | None |
| pycountry | Pure Python | B | None |
| schedule | Pure Python | B | None |
| distro | Pure Python | B | None |
| certifi | Pure Python | B | None |
| charset-normalizer | Pure Python | B | None |
| idna | Pure Python | B | None |
| numpy | C Extension | C | Dynamic loading |
| pandas | C Extension | D | numpy |
| scipy | C Extension | D | numpy |
| Pillow | C Extension | D | Dynamic loading, libjpeg/libpng |
| lxml | C Extension | C | Dynamic loading, libxml2/libxslt |
| matplotlib | C Extension | D | numpy, freetype |
| seaborn | Pure Python | B | matplotlib |
| psutil | C Extension | C | Dynamic loading, /proc filesystem |
| cryptography | C Extension | C | Dynamic loading, OpenSSL (already ported) |
| rapidfuzz | C Extension | C | Dynamic loading |
| sympy | Pure Python | B | None (large; depends on mpmath) |
| plotnine | Pure Python | B | matplotlib, numpy, pandas |
| altair | Pure Python | B | Jinja2, pandas |
| wordcloud | C Extension | D | numpy, Pillow |
| moviepy | Pure Python | E | fork/exec + ffmpeg |
| pydub | Pure Python | E | fork/exec + ffmpeg |
| ffmpeg-python | Pure Python | E | fork/exec + ffmpeg |
| pytesseract | Pure Python | E | fork/exec + tesseract |
| requests | Pure Python | F | TCP/IP sockets |
| urllib3 | Pure Python | F | TCP/IP sockets |
| httpx | Pure Python | F | TCP/IP sockets |
| feedparser | Pure Python | F | TCP/IP sockets |
| pyperclip | Pure Python | F | No clipboard backend on headless Nanvix |

---
