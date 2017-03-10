from setuptools import find_packages, setup

setup(
    name='django-digitaldiocese-worthers',
    packages=find_packages(),
    version='0.0.1',
    author='Blanc Ltd',
    author_email='studio@blanc.ltd.uk',
    description='Python client for the Church of England CMS API',
    license='BSD',
    url='https://github.com/blancltd/django-digitaldiocese-worthers',
    include_package_data=True,
    install_requires=[
        'requests>=2.0.0',
    ],
)
