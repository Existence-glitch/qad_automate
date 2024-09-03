from setuptools import setup, find_packages

setup(
    name="qad-automation-tool",
    version="1.01",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "paramiko==3.4.1",
        "invoke==2.2.0",
        "fabric==3.2.2",
        "python-dotenv==1.0.1",
        "pyyaml==6.0.2",
        "gspread==6.1.2",
    ],
    entry_points={
        "console_scripts": [
            "qad-automation=main:main",
        ],
    },
    author="Joaquín Tapia Riquelme",
    author_email="joaquintapia.inf@gmail.com",
    description="An automation tool for QAD systems",
    long_description=open("docs/README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Existence-glitch/qad_automate",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
)