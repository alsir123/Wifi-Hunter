from unittest import mock

import menu_install_tools as mit


def test_option_formats_name_and_number(capsys):
    mit.option("Aircrack-ng", 2)
    out = capsys.readouterr().out
    assert "Aircrack-ng" in out
    assert "2" in out


def test_menu_lists_all_ten_tools(capsys):
    mit.menu()
    out = capsys.readouterr().out
    for tool in ["Wifte", "Aircrack-ng", "Reaver", "Pixiewps", "Wireshark",
                 "Wash", "Macchanger", "Cowpatty", "Bully", "Mdk3"]:
        assert tool in out


def test_choice_install_tools_yes_runs_apt_commands():
    with mock.patch("builtins.input", side_effect=["y", "n"]), \
            mock.patch.object(mit.os, "system") as mock_system:
        mit.choice_intall_tools()
    called = " ".join(call.args[0] for call in mock_system.call_args_list)
    assert "sudo apt-get update" in called
    assert "pixiewps" in called
    assert "aircrack-ng" in called
    assert "mdk3" in called


def test_choice_install_tools_yes_back_home_runs_main():
    with mock.patch("builtins.input", side_effect=["y", "y"]), \
            mock.patch.object(mit.os, "system") as mock_system:
        mit.choice_intall_tools()
    called = [call.args[0] for call in mock_system.call_args_list]
    assert "python3 main.py" in called


def test_choice_install_tools_no_clears_screen(capsys):
    with mock.patch("builtins.input", side_effect=["n"]), \
            mock.patch.object(mit.os, "system") as mock_system:
        mit.choice_intall_tools()
    mock_system.assert_called_once_with("clear")
    assert "Wrong try again!" in capsys.readouterr().out
