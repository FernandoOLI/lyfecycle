from files.polices_generator import ignore_delta_log, polices_generator
from unittest.mock import patch

@patch("files.polices_generator.get_valid_lifecycle_paths")
@patch("files.polices_generator.ignore_delta_log")
@patch("files.polices_generator.save_file")
def test_polices_generator(mock_save_file, mock_ignore_delta_log, mock_get_paths):
    test_data = {
        "name": "test_config.json",
        "prefix": "data",
        "days_to_glacier": 30,
        "days_to_deep_archive": 90,
        "days_to_expiration": 180
    }

    mock_get_paths.return_value = ["s3://bucket/data"]
    mock_ignore_delta_log.return_value = [
        {
            "ID": "MockRule",
            "Prefix": "mock/",
            "Status": "Enabled"
        }
    ]

    polices_generator(test_data)

    mock_get_paths.assert_called_once_with("test_config.json", "data")
    mock_ignore_delta_log.assert_called_once_with(["s3://bucket/data"])
    mock_save_file.assert_called_once()

    expected_final_rule = {
        "ID": "Default-Transition-Policy",
        "Filter": {"Prefix": "data"},
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

    mock_save_file.assert_called_once_with(expected_config, "test_config.json")

def test_ignore_delta_log():
    input_data =  [
            "s3://my-bucket/data/test",
            "s3://my-bucket/data/test2/test2"
        ]


    expected_output = [
        {
            "ID": "ExcludeDeltaLog-data-test",
            "Filter": {"Prefix": "s3://my-bucket/data/test/_delta_log/"},
            "Status": "Enabled",
            "Expiration": {"Days": 9999}
        },
        {
            "ID": "ExcludeDeltaLog-data-test2-test2",
            "Filter": {"Prefix": "s3://my-bucket/data/test2/test2/_delta_log/"},
            "Status": "Enabled",
            "Expiration": {"Days": 9999}
        }
    ]

    result = ignore_delta_log(input_data)

    assert result == expected_output
