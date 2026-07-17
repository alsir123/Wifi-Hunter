import spam_wifi


def test_main_option_formats_number_and_name(capsys):
    spam_wifi.main_option(1, "Use Random SSIDS (slow)")
    out = capsys.readouterr().out
    assert "1" in out
    assert "Use Random SSIDS (slow)" in out


def test_main_option_zero_exit_entry(capsys):
    spam_wifi.main_option(0, "Exit")
    out = capsys.readouterr().out
    assert "0" in out
    assert "Exit" in out
