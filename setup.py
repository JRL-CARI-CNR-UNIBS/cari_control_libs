from setuptools import setup, find_packages

setup(
    name='cari_control_libs',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,  # ← enables inclusion of data files
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        # add other dependencies here
    ],
    author='Manuel Beschi',
    author_email='manuel.beschi@unibs.it',
    description='Control library in Python of the JRL-CARI',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/JRL-CARI-CNR-UNIBS/cari_control_libs',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
    ],
    python_requires='>=3.7',
)
