import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ar_mobile_parce",
    version="0.0.3",
    author="filoquin",
    author_email="filquin@sipecu.com.ar",
    description="Parce mobiles argentine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={
        'ar_mobile_parce': ['ar_mobile_parce/enacom.csv','ar_mobile_parce/cp_indicativos.csv'],
    },
    url="https://github.com/filoquin/ar_mobile_parce",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)