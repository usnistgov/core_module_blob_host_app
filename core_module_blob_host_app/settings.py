""" Core module blob host app settings

Settings with the following syntax can be overwritten at the project level:
SETTING_NAME = getattr(settings, "SETTING_NAME", "Default Value")
"""
from django.conf import settings

if not settings.configured:
    settings.configure()

INSTALLED_APPS = getattr(settings, "INSTALLED_APPS", [])
""" list: List of installed apps.
"""

AUTO_ESCAPE_XML_ENTITIES = getattr(settings, "AUTO_ESCAPE_XML_ENTITIES", True)
""" bool: enable or not the auto escape of the XML predefined entities.
"""

SERVER_URI = getattr(settings, "SERVER_URI", "http://localhost")
""" str: Application URI.
"""
