from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='1',
    description='Cleans your foder',
    url='http://github.com/dummy_user/useful',
    author='Flying Circus',
    author_email='flyingcircus@example.com',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
)