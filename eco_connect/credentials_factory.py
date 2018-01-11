import os


class CredentialsFactory:

    def get_env_var(self, variable):
        return os.environ.get(variable, None)

    def get_eco_credentials(self):
        return (self.get_env_var('ECO_CONNECT_USER'),
                self.get_env_var('ECO_CONNECT_PASSWORD'))
