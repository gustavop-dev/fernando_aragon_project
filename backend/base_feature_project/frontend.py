"""Serve SPA documents through Django so hosting controls also cover direct URLs."""
from pathlib import Path

from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from django.http import Http404, HttpResponse
from django.utils._os import safe_join
from django.views.static import serve


def frontend(request, path=''):
    root = Path(settings.BASE_DIR).parent / 'frontend' / 'dist'
    try:
        candidate = Path(safe_join(root, path))
    except SuspiciousFileOperation:
        raise Http404 from None
    if candidate.is_file() and candidate.suffix.lower() != '.html':
        return serve(request, path, document_root=root)
    if candidate.is_file():
        page = candidate
    elif not Path(path).suffix:
        page = root / 'index.html'
    else:
        raise Http404
    try:
        return HttpResponse(page.read_text(encoding='utf-8'), content_type='text/html; charset=utf-8')
    except OSError:
        raise Http404 from None
