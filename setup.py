"""
Setup.
"""
from setuptools import find_packages, setup


setup(
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description='PDBE is a tool, that put import pdb statement everywhere you want and clear it in the same way.',
    entry_points={
        'console_scripts': [
            'pdbe = pdbe.cli:pdbe',
        ]
    },
    license='MIT',
    name='pdbe',
    packages=find_packages(),
    include_package_data=True,
    version='0.2.0',
)
