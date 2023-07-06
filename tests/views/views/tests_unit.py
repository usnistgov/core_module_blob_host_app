""" Unit tests for core_module_blob_host_app views.
"""
from unittest import TestCase
from unittest.mock import patch, Mock
from urllib.parse import urljoin

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
from core_module_blob_host_app.views import views as blob_host_views
from tests.test_settings import SERVER_URI


class TestBlobHostModuleRetrievePostData(TestCase):
    """Unit tests for `BlobHostModule.retrieve_post_data` method."""

    def setUp(self) -> None:
        """setUp"""
        self.request = create_mock_request()
        self.request.POST = {}
        self.request.FILES = {"file": Mock()}
        self.request.user = create_mock_user(1)

    @patch.object(blob_host_views, "BLOBHostForm")
    def test_blob_host_form_called(self, mock_blob_host_form):
        """test_blob_host_form_called"""
        blob_host_module = blob_host_views.BlobHostModule()

        blob_host_module.retrieve_post_data(self.request)
        mock_blob_host_form.assert_called_with(
            self.request.POST, self.request.FILES
        )

    @patch.object(blob_host_views, "BLOBHostForm")
    def test_form_not_valid_returns_empty_data(self, mock_blob_host_form):
        """test_form_not_valid_returns_empty_data"""
        mock_blob_host_form_object = Mock()
        mock_blob_host_form_is_valid = Mock()
        mock_blob_host_form_is_valid.return_value = False
        mock_blob_host_form_object.is_valid = mock_blob_host_form_is_valid
        mock_blob_host_form.return_value = mock_blob_host_form_object

        blob_host_module = blob_host_views.BlobHostModule()
        response = blob_host_module.retrieve_post_data(self.request)
        self.assertEqual(response, "")

    @patch.object(blob_host_views, "blob_api")
    @patch.object(blob_host_views, "Blob")
    @patch.object(blob_host_views, "BLOBHostForm")
    def test_blob_api_insert_called(
        self, mock_blob_host_form, mock_blob, mock_blob_api
    ):
        """test_blob_api_insert_called"""
        mock_blob_host_form_object = Mock()
        mock_blob_host_form_is_valid = Mock()
        mock_blob_host_form_is_valid.return_value = True
        mock_blob_host_form_object.is_valid = mock_blob_host_form_is_valid
        mock_blob_host_form.return_value = mock_blob_host_form_object

        mock_blob_object = Mock()
        mock_blob.return_value = mock_blob_object

        blob_host_module = blob_host_views.BlobHostModule()
        blob_host_module.retrieve_post_data(self.request)

        mock_blob_api.insert.assert_called_with(
            mock_blob_object, self.request.user
        )

    @patch.object(blob_host_views, "blob_api")
    @patch.object(blob_host_views, "Blob")
    @patch.object(blob_host_views, "BLOBHostForm")
    def test_blob_api_insert_exception_returns_empty_data(
        self, mock_blob_host_form, mock_blob, mock_blob_api
    ):
        """test_blob_api_insert_exception_returns_empty_data"""
        mock_blob_host_form_object = Mock()
        mock_blob_host_form_is_valid = Mock()
        mock_blob_host_form_is_valid.return_value = True
        mock_blob_host_form_object.is_valid = mock_blob_host_form_is_valid
        mock_blob_host_form.return_value = mock_blob_host_form_object
        mock_blob_object = Mock()
        mock_blob.return_value = mock_blob_object
        mock_blob_api.insert.side_effect = Exception(
            "mock_blob_api_insert_exception"
        )

        blob_host_module = blob_host_views.BlobHostModule()
        response = blob_host_module.retrieve_post_data(self.request)

        self.assertEqual(response, "")

    @patch.object(blob_host_views, "get_blob_download_uri")
    @patch.object(blob_host_views, "settings")
    @patch.object(blob_host_views, "blob_api")
    @patch.object(blob_host_views, "Blob")
    @patch.object(blob_host_views, "BLOBHostForm")
    def test_default_returns_blob_download_uri(
        self,
        mock_blob_host_form,
        mock_blob,
        mock_blob_api,
        mock_settings,
        mock_get_blob_download_uri,
    ):
        """test_default_returns_blob_download_uri"""
        mock_blob_host_form_object = Mock()
        mock_blob_host_form_is_valid = Mock()
        mock_blob_host_form_is_valid.return_value = True
        mock_blob_host_form_object.is_valid = mock_blob_host_form_is_valid
        mock_blob_host_form.return_value = mock_blob_host_form_object
        mock_blob_object = Mock()
        mock_blob.return_value = mock_blob_object
        mock_blob_api.insert.return_value = None
        expected_response = "mock_get_blob_download_uri"
        mock_get_blob_download_uri.return_value = expected_response
        mock_settings_object = Mock()
        mock_settings_object.INSTALLED_APPS = []
        mock_settings.return_value = mock_settings_object

        blob_host_module = blob_host_views.BlobHostModule()
        response = blob_host_module.retrieve_post_data(self.request)

        self.assertEqual(response, expected_response)

    @patch("core_linked_records_app.components.blob.api")
    @patch.object(blob_host_views, "reverse")
    @patch("core_linked_records_app.components.pid_settings.api.get")
    @patch.object(blob_host_views, "blob_api")
    @patch.object(blob_host_views, "Blob")
    @patch.object(blob_host_views, "BLOBHostForm")
    def test_linked_record_in_apps_returns_blob_pid(
        self,
        mock_blob_host_form,
        mock_blob,
        mock_blob_api,
        mock_pid_settings_api,
        mock_reverse,
        mock_pid_blob_api,
    ):
        """test_linked_record_in_apps_returns_blob_pid"""
        mock_blob_host_form_object = Mock()
        mock_blob_host_form_is_valid = Mock()
        mock_blob_host_form_is_valid.return_value = True
        mock_blob_host_form_object.is_valid = mock_blob_host_form_is_valid
        mock_blob_host_form.return_value = mock_blob_host_form_object
        mock_blob_object = Mock()
        mock_blob.return_value = mock_blob_object
        mock_blob_api.insert.return_value = None
        mock_pid_settings = Mock()
        mock_pid_settings.auto_set_pid = True
        mock_pid_settings_api.get.return_value = mock_pid_settings
        blob_pid_url = "mock_blob_pid_url"
        mock_reverse.return_value = blob_pid_url
        mock_pid_blob_api.get_pid_for_blob.return_value = Mock()

        blob_host_module = blob_host_views.BlobHostModule()
        response = blob_host_module.retrieve_post_data(self.request)

        self.assertEqual(response, urljoin(SERVER_URI, blob_pid_url))
