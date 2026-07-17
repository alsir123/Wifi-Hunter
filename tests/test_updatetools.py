from unittest import mock

import updatetools


def test_get_remote_version_parses_json():
    fake_response = mock.Mock()
    fake_response.json.return_value = {"version": 5}
    with mock.patch.object(updatetools.requests, "get", return_value=fake_response) as mock_get:
        assert updatetools.get_remote_version("http://example.com") == 5
    mock_get.assert_called_once_with("http://example.com")


def test_get_remote_version_uses_default_url():
    fake_response = mock.Mock()
    fake_response.json.return_value = {"version": 3}
    with mock.patch.object(updatetools.requests, "get", return_value=fake_response) as mock_get:
        assert updatetools.get_remote_version() == 3
    mock_get.assert_called_once_with(updatetools.DATABASE_URL)


def test_read_local_version_reads_first_line_as_int(tmp_path):
    version_file = tmp_path / "version"
    version_file.write_text("9\n")
    assert updatetools.read_local_version(str(version_file)) == 9
