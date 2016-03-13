import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()


setup(
    name='ru_number_to_text',
    version='0.1',
    author='Sergey Prokhorov',
    author_email='me@seriyps.ru',
    url='https://github.com/seriyps/ru_number_to_text',
    keywords='plural forms',
    test_suite='tests',
    packages=find_packages(),
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
)
