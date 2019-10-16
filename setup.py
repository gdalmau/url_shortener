from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    INSTALL_REQUIRES = f.readlines()

setup(
    name='url_shortener',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/gdalmau/url_shortener',
    license='MIT',
    author='Gerard Dalmau',
    description='Webservice to shorten URLs',
    install_requires=INSTALL_REQUIRES
)
