from django.apps import AppConfig


class CatalogConfig(AppConfig):
    """Base configuration class for Catalog application"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
