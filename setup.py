from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ic_basilisk_os",
    version="0.1.0",
    author="Smart Social Contracts",
    author_email="contact@smartsocialcontracts.org",
    description="Basilisk OS — Operating system services, shell, and SFTP for IC Python canisters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smart-social-contracts/ic-basilisk-os",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10",
    install_requires=[
        "ic-basilisk>=0.11.0",
        "ic-python-db>=0.7.7",
        "ic-python-logging>=0.3.1",
    ],
    extras_require={
        "shell": ["asyncssh"],
        "test": ["pytest>=7.0.0", "pytest-cov>=4.0.0"],
    },
    entry_points={
        "console_scripts": [
            "basilisk-os=ic_basilisk_os.cli:main",
        ],
    },
)
