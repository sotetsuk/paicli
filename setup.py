from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='paicli',
    version="0.5.5",
    description='Client for PAI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sotetsu KOYAMADA',
    url='',
    author_email='koyamada-s@sys.i.kyoto-u.ac.jp',
    license='MIT',
    install_requires=["requests",
                      "pyyaml",
                      "prompt_toolkit==1.0.9",
                      "prettytable",
                      "termcolor",
                      "colorama",
                      "click",
                      ],
    packages=find_packages(),
    entry_points={
        'console_scripts': 'pai = paicli.main:main'
    },
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License"
    ]
)
