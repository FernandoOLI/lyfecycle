from unittest.mock import mock_open, patch, call
from files.bash_generate import bash_command_generate


@patch("builtins.open", new_callable=mock_open)
def test_bash_generate(mock_file):
    bash_command_generate("my-bucket.json")

    mock_file.assert_called_with("output/bash/lifecycle.sh", "a")

    handle = mock_file()
    handle.write.assert_any_call("echo Applying lifecycle to bucket: my-bucket\n")
