from setuptools import find_packages, setup

setup(
    name='django-digitaldiocese',
    packages=find_packages(),
    version='1.5.8',
    author='Blanc Ltd',
    author_email='studio@blanc.ltd.uk',
    description='Handbook',
    license='BSD',
    url='https://github.com/blancltd/django-digitaldiocese',
    include_package_data=True,
    install_requires=[
        'tqdm>=4.9.0',
    ],
)
