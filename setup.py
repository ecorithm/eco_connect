from setuptools import setup, find_packages
import versioneer


def get_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name='eco-connect',
    version='0.16.0',
    license="Proprietary",
    url='https://github.com/ecorithm/eco-connect',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=get_requirements(),
    cmdclass=versioneer.get_cmdclass()
)
