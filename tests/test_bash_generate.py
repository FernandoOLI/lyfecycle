from unittest.mock import mock_open, patch, call
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

    expected_calls = [
        call("#!/bin/bash\n\n"),
        call("echo Applying lifecycle to bucket: my-bucket\n"),
        call('SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"\n'),
        call('JSON_FILE="$SCRIPT_DIR/../rules/test_lifecycle.json"\n'),
        call("aws s3api put-bucket-lifecycle-configuration \\\n"),
        call("  --bucket my-bucket \\\n"),
        call("  --lifecycle-configuration file://$JSON_FILE\n")
    ]

    handle.write.assert_has_calls(expected_calls, any_order=False)
