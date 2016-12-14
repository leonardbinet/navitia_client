try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='navitia-python',
    packages=['navitia-python'],  # this must be the same as the name above
    version='0.1',
    description='Navitia client for python',
    author='Leonard Binet',
    author_email='leonardbinet@gmail.com',
    url='https://github.com/leonardbinet/navitia-python',
    classifiers=[],
)
