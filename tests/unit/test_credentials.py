from eco_connect import validate_credentials


def test_validate_credentials_200(mocker):
    mock_os = mocker.patch("eco_connect.os")
    mock_os.environ.get.return_value = "mock-cred"
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mocker.patch("eco_connect.requests.get", return_value=mock_response)
    result = validate_credentials()
    assert result


def test_validate_credentials_401(mocker):
    mock_os = mocker.patch("eco_connect.os")
    mock_os.environ.get.return_value = "mock-cred"
    mock_response = mocker.Mock()
    mock_response.status_code = 401
    mocker.patch("eco_connect.requests.get", mock_response)
    result = validate_credentials()
    assert result is False
