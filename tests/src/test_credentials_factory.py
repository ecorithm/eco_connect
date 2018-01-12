from eco_connect.src.credentials_factory import CredentialsFactory


class TestCredentialsFactory:
    MODULE_PATH = 'eco_connect.src.credentials_factory'

    CLASS_PATH = MODULE_PATH + '.CredentialsFactory'

    def test_get_env_var(self, mocker):
        mock_os = mocker.patch(self.MODULE_PATH + '.os.environ.get',
                               return_value='TEST_VAL')

        result = CredentialsFactory.get_env_var('TEST_NAME')

        mock_os.assert_called_once_with('TEST_NAME', None)

        assert result == 'TEST_VAL'

    def test_get_env_var_does_not_exist(self, mocker):

        result = CredentialsFactory.get_env_var('MISSING_NAME')

        assert result is None

    def test_get_eco_credentials(self, mocker):
        mock_get_env_var = mocker.patch(self.CLASS_PATH + '.get_env_var',
                                        return_value='TEST_VAL')

        result = CredentialsFactory.get_eco_credentials()

        assert mock_get_env_var.call_count == 2
        assert mock_get_env_var.called_with('TEST_VAL', None)
        assert result == ('TEST_VAL', 'TEST_VAL')
