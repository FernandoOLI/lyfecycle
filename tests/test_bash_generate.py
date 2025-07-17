from unittest.mock import mock_open, patch
from files.bash_generate import bash_generate


@patch("files.util.open_config_file")
@patch("builtins.open", new_callable=mock_open)
def test_bash_generate(mock_file, mock_open_config):
    mock_open_config.return_value = {'bucket_name': 'my-bucket'}
    test_file = "test_config.json"
    bash_generate(test_file)
    mock_open_config.assert_called_once_with(test_file)
    mock_file.assert_called_once_with("output/bash/lifecycle.sh", "a")

    handle = mock_file()

    expected_lines = [
        "\n",
        "echo Applying lifecycle to bucket: my-bucket \n\n",
        "aws s3api put-bucket-lifecycle-configuration \\\n",
        "--bucket my-bucket \\\n",
        "--lifecycle-configuration file://../rules/test_lifecycle.json\n"
    ]

    handle.writelines.assert_called_once_with(expected_lines)


