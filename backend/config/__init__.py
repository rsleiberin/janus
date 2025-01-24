"""
Configuration module for the Flask application.

This module exports a dictionary `config_by_name` that maps configuration names
to their respective configuration classes.
"""

from .development import DevelopmentConfig
from .testing import TestingConfig
from .production import ProductionConfig

config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
