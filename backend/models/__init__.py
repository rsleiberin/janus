"""
Initializes the models package, making it easy to import model classes in one place.

Note:
    We do *not* re-export 'db' here because we prefer importing it directly
    from 'backend.db' rather than from 'backend.models'.
"""

from .user import User
from .admin import Admin
from .image import Image
from .image_analysis import ImageAnalysis
from .log import Log
from .analytics import Analytics
from .security import Security

__all__ = [
    "User",
    "Admin",
    "Image",
    "ImageAnalysis",
    "Log",
    "Analytics",
    "Security",
]
