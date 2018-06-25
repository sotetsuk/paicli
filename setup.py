from setuptools import setup, find_packages

setup(
    name='paicli',
    version="0.3.0",
    description='Client for PAI',
    author='Sotetsu KOYAMADA',
    url='',
    author_email='koyamada-s@sys.i.kyoto-u.ac.jp',
    license='MIT',
    install_requires=["requests",
                      "pyyaml",
                      "prompt_toolkit==1.0.9",
                      "prettytable",
                      "termcolor",
                      "click",
                      ],
    packages=find_packages(),
    entry_points={
        'console_scripts': 'paicli = paicli.main:main'
    },
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License"
    ]
)
