""" Blob host module
"""
import re
from core_module_blob_host_app.settings import AUTO_ESCAPE_XML_ENTITIES
from core_main_app.components.blob import api as blob_api
from core_main_app.components.blob.models import Blob
from core_main_app.components.blob.utils import get_blob_download_uri
from core_module_blob_host_app.views.forms import BLOBHostForm
from core_parser_app.tools.modules.views.builtin.popup_module import AbstractPopupModule
from core_parser_app.tools.modules.views.module import AbstractModule
from xml_utils.xsd_tree.operations.xml_entities import XmlEntities


class BlobHostModule(AbstractPopupModule):
    """BLOB host module"""

    def __init__(self):
        """Initialize module"""
        AbstractPopupModule.__init__(
            self,
            button_label="Upload File",
            scripts=["core_module_blob_host_app/js/blob_host.js"],
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
        return AbstractModule.render_template(
            "core_module_blob_host_app/blob_host.html",
            {
                "form": form,
                "module_id": module_id,
            },
        )

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
            try:
                form = BLOBHostForm(request.POST, request.FILES)
                if not form.is_valid():
                    self.error = "No file uploaded."
                    return data

                # get file from request
                uploaded_file = request.FILES["file"]
                # get filename from file
                filename = uploaded_file.name
                # get user id from request
                user_id = str(request.user.id)

                # create blob
                blob = Blob(filename=filename, user_id=user_id)
                # set blob file
                blob.blob = uploaded_file
                # save blob
                blob_api.insert(blob)
                # get download uri
                data = get_blob_download_uri(blob, request)
            except:
                self.error = "An unexpected error occurred."

        return (
            data_xml_entities.escape_xml_entities(data)
            if AUTO_ESCAPE_XML_ENTITIES
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

        Args:
            data:
            error:

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
