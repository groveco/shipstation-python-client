from setuptools import setup, find_packages


setup(
    name='shipstation-python',
    version='0.0.1',
    description='Python client for the ShipStation REST API',
    url='https://github.com/groveco/shipstation-python-client',
    keywords=['shipstation'],
    install_requires=['requests>=2.3.0'],
    packages=find_packages(),
    include_package_data=True,
)
