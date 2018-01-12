# eco-connect
A wrapper for connecting to Ecorithm's API Platform through python

## Requirements
- The package can be installed using pip.
  `pip3 install git+git://github.com/ecorithm/eco-connect.git@master --upgrade
`
- This module requires authentication for the connectors to be use. Credentials are loaded through your environment variables. Create the following env variables with your provided ecorithm credentials:
`export ECO_CONNECT_USER=MyEcorithmUserName`
`export ECO_CONNECT_PASSWORD=MyEcorithmPASSWord`

- To test the your credentials open a python interpreter and run the following:
`from  eco_connect import validate_credentials`
`validate_credentials()`


## Usage
- Supported ecorithm connectors include:
* FactsService

- To use, import the connector i.e `from eco_connect import FactsService`

- For additional resources please refer to documentation at `https://django.prod.ecorithm.com/`
or contact support at `help@ecorithm.com`
