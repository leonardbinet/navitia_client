try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='navitia_client',
    packages=['navitia_client'],
    version='0.4',
    description='Navitia client for python',
    author='Leonard Binet',
    author_email='leonardbinet@gmail.com',
    license='MIT',
    url='https://github.com/leonardbinet/navitia-python',
    classifiers=[],
)
