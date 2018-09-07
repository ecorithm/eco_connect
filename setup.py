from setuptools import setup

with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name='eco-connect',
    version='0.24.1',
    description='Ecorithm\'s connector to Facts Service',
    long_description=readme,
    long_description_content_type='text/x-rst',
    author="Ecorithm",
    author_email="support@ecorithm.com",
    url='https://ecorithm.com',
    packages=['eco_connect'],
    package_data={'': ['LICENSE']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=['pandas'],
    license='MIT',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering'
    ],
    project_urls={
        "Documentation": "http://eco-connect.readthedocs.io/en/latest/",
        "Source Code": "https://github.com/ecorithm/eco_connect",
    },
    extras_require={
        'docs': [
            'sphinx',
            'sphinx_rtd_theme'
        ]
    }

)
