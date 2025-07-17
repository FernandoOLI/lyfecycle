from files.polices_generator import ignore_delta_log, polices_generator
from unittest.mock import patch


@patch("files.util.open_config_file")
@patch("files.polices_generator.ignore_delta_log")
@patch("files.polices_generator.save_file")
def test_polices_generator(mock_save_file, mock_ignore_delta_log, mock_open_config):
    test_file = "test_config.json"

    mock_open_config.return_value = {
        "paths": ["s3://my-bucket/data"],
        "days_to_glacier": 30,
        "days_to_deep_archive": 90,
        "days_to_expiration": 180
    }

    mock_ignore_delta_log.return_value = [
        {
            "ID": "MockRule",
            "Prefix": "mock/",
            "Status": "Enabled"
        }
    ]

    polices_generator(test_file)

    mock_open_config.assert_called_once_with(test_file)
    mock_ignore_delta_log.assert_called_once_with(mock_open_config.return_value)

    expected_final_rule = {
        "ID": "Default-Transition-Policy",
        "Filter" : {"Prefix": "data"},
        "Status": "Enabled",
        "Transitions": [
            {"Days": 30, "StorageClass": "GLACIER"},
            {"Days": 90, "StorageClass": "DEEP_ARCHIVE"}
        ],
        "Expiration": {"Days": 180}
    }

    expected_config = {
        "Rules": [
            {
                "ID": "MockRule",
                "Prefix": "mock/",
                "Status": "Enabled"
            },
            expected_final_rule
        ]
    }

    mock_save_file.assert_called_once_with(expected_config, test_file)


def test_ignore_delta_log():
    input_data = {
        "paths": [
            "s3://my-bucket/data/test/",
            "s3://my-bucket/data/test2/test2/"
        ]
    }

    expected_output = [
        {
            "ID": "ExcludeDeltaLog-test",
            "Filter": {"Prefix": "s3://my-bucket/data/test/_delta_log/"},
            "Status": "Enabled"
        },
        {
            "ID": "ExcludeDeltaLog-test2",
            "Filter": {"Prefix": "s3://my-bucket/data/test2/test2/_delta_log/"},
            "Status": "Enabled"
        }
    ]

    result = ignore_delta_log(input_data)

    assert result == expected_output
