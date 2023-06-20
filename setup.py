import setuptools

# with open("README.md", "r") as fh:
#    long_description = fh.read()

# https://packaging.python.org/tutorials/packaging-projects/
setuptools.setup(
    name='annotest',
    version='0.1',
    author="Moe",
    author_email="",
    description="",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    # url="https://github.com/.....",
    packages=setuptools.find_packages(exclude=('tests')),
    install_requires=[
        "astor~=0.8.1",
        "autoflake~=1.4",
        "hypothesis~=6.4",
    ],
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    # ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'annotest = annotest.__main__:main'
        ]
    })
