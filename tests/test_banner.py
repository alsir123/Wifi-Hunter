from unittest import mock

import banner


def test_banner_constant_contains_metadata():
    assert "Team Dark Hunter 141" in banner.banner
    assert "Version: 1.0" in banner.banner


def test_banners_clears_and_prints(capsys):
    with mock.patch.object(banner.os, "system") as mock_system:
        banner.banners()
    mock_system.assert_called_once_with("clear")
    out = capsys.readouterr().out
    assert "Team Dark Hunter 141" in out
    assert "_" * 55 in out
