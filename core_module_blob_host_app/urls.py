""" Url router for the blob host module
"""

from django.urls import re_path

from core_module_blob_host_app.views.views import BlobHostModule

urlpatterns = [
    re_path(
        r"module-blob-host", BlobHostModule.as_view(), name="core_module_blob_host_view"
    ),
]
