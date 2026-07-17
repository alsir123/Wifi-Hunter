from unittest import mock

import main


def test_main_option_formats_number_and_name(capsys):
    main.main_option(2, "Wifi Spam")
    out = capsys.readouterr().out
    assert "2" in out
    assert "Wifi Spam" in out


def test_get_remote_version_parses_json():
    fake_response = mock.Mock()
    fake_response.json.return_value = {"version": 7}
    with mock.patch.object(main.requests, "get", return_value=fake_response) as mock_get:
        assert main.get_remote_version("http://example.com") == 7
    mock_get.assert_called_once_with("http://example.com")


def test_get_remote_version_uses_default_url():
    fake_response = mock.Mock()
    fake_response.json.return_value = {"version": 1}
    with mock.patch.object(main.requests, "get", return_value=fake_response) as mock_get:
        assert main.get_remote_version() == 1
    mock_get.assert_called_once_with(main.DATABASE_URL)


def test_read_local_version_reads_first_line_as_int(tmp_path):
    version_file = tmp_path / "version"
    version_file.write_text("42\n")
    assert main.read_local_version(str(version_file)) == 42
