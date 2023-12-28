from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='1',
    description='Sort files in your folder',
    url='https://github.com/RHA1705/HW7.git',
    author='Roman Harbazh',
    author_email='garbarzroman47@gmail.com',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
)