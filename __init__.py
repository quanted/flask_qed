from __future__ import absolute_import, unicode_literals

# although this is a git submodule of qed, it actually runs a separate flask server
# https://stackoverflow.com/questions/3073259/python-nose-import-error/3073368#3073368

from .celery_cgi import celery

__all__ = ['celery']
