import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apiscrub",
    version="1.0.0",
    author="Daniel G. Taylor",
    author_email="danielgtaylor@gmail.com",
    description="OpenAPI Scrubber",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielgtaylor/apiscrub",
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
