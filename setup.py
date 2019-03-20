import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apiscrub",
    version="1.2.0",
    author="Daniel G. Taylor",
    author_email="danielgtaylor@gmail.com",
    description="OpenAPI Scrubber",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielgtaylor/apiscrub",
    install_requires=[
        'ruamel.yaml>=0.15.89',
    ],
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'apiscrub=apiscrub.main:run',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
