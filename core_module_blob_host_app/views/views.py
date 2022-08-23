""" Blob host module
"""
import logging
import re
from urllib.parse import urljoin

from django.urls import reverse

from core_main_app.components.blob import api as blob_api
from core_main_app.components.blob.models import Blob
from core_main_app.components.blob.utils import get_blob_download_uri
from core_parser_app.tools.modules.views.builtin.popup_module import AbstractPopupModule
from core_parser_app.tools.modules.views.module import AbstractModule
from xml_utils.xsd_tree.operations.xml_entities import XmlEntities
from core_module_blob_host_app import settings as blob_host_settings
from core_module_blob_host_app.views.forms import BLOBHostForm

logger = logging.getLogger(__name__)


class BlobHostModule(AbstractPopupModule):
    """BLOB host module"""

    def __init__(self):
        """Initialize module"""
        super().__init__(
            button_label="Upload File",
            scripts=[
                "core_parser_app/js/commons/file_uploader.js",
                "core_module_blob_host_app/js/blob_host.js",
            ],
        )

    def _get_popup_content(self):
        """Return popup content

        Returns:

        """
        module_id = None

        if self.request:
            module_id = self.request.GET.get("module_id", None)

        # create the from and set an unique id
        form = BLOBHostForm()
        form.fields["file"].widget.attrs.update(
            {"id": "file-input-%s" % str(module_id)}
        )
        return super().render_template(
            "core_module_blob_host_app/blob_host.html",
            {
                "form": form,
                "module_id": module_id,
            },
        )

    def retrieve_post_data(self, request):
        """retrieve_post_data
        Args:
            request:

        Returns:
        """
        data = ""
        try:
            form = BLOBHostForm(request.POST, request.FILES)
            if not form.is_valid():
                self.error = "No file uploaded."
                return data

            uploaded_file = request.FILES["file"]

            # Create blob
            blob = Blob(
                filename=uploaded_file.name,
                user_id=str(request.user.id) if request.user.id else None,
            )
            blob.blob = uploaded_file
            blob_api.insert(blob, request.user)

            blob_pid = None

            # Retrieve Blob PID if the core_linked_records_app is installed
            if "core_linked_records_app" in blob_host_settings.INSTALLED_APPS:
                from core_linked_records_app.components.pid_settings import (
                    api as pid_settings_api,
                )
                from core_linked_records_app.components.blob import (
                    api as linked_records_blob_api,
                )

                # Create blob PID if `auto_set_pid` is True
                if pid_settings_api.get().auto_set_pid:
                    blob_pid_url = reverse(
                        "core_linked_records_provider_record",
                        kwargs={
                            "provider": "local",
                            "record": linked_records_blob_api.get_pid_for_blob(
                                str(blob.id)
                            ).record_name,
                        },
                    )
                    blob_pid = urljoin(blob_host_settings.SERVER_URI, blob_pid_url)

            # Retrieve download URI.
            return blob_pid if blob_pid else get_blob_download_uri(blob, request)
        except Exception as exc:
            logger.log(str(exc))
            self.error = "An unexpected error occurred."
            return data

    def _retrieve_data(self, request):
        """Retrieve module's data

        Args:
            request:

        Returns:

        """
        data = ""
        self.error = None
        data_xml_entities = XmlEntities()
        if request.method == "GET":
            if "data" in request.GET:
                if len(request.GET["data"]) > 0:
                    data = request.GET["data"]
        elif request.method == "POST":
            data = self.retrieve_post_data(request)

        return (
            data_xml_entities.escape_xml_entities(data)
            if blob_host_settings.AUTO_ESCAPE_XML_ENTITIES
            else data
        )

    def _render_data(self, request):
        """Return module's data rendering

        Args:
            request:

        Returns:

        """
        return BlobHostModule.render_blob_host_data(self.data, self.error)

    @staticmethod
    def render_blob_host_data(data, error):
        """Render blob host data

        Returns:

        """
        context = {}
        if error is not None:
            context["error"] = error
        else:
            """We have to unescape the string before the graphical render"""
            context["handle"] = XmlEntities.unescape_xml_entities(data)[0]

        """Even if we have unescaped the graphical version of the data
         we have to display the warning message if there are xml predefined entities"""
        data_xml_entities = XmlEntities()
        data_xml_entities.escape_xml_entities(data)
        if (
            data_xml_entities.number_of_subs_made > 0
            or len(re.findall(r"((&amp;)|(&gt;)|(&lt;)|(&apos;)|(&quot;))", data)) > 0
        ):
            context["xml_entities_warning"] = True

        return AbstractModule.render_template(
            "core_module_blob_host_app/blob_host_display.html", context
        )
