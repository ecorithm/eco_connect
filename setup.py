from setuptools import setup


def get_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name='eco-connect',
    version='0.1',
    packages=['eco_connect'],
    include_package_data=True,
    install_requires=get_requirements()
)
