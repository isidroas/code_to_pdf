import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="code_to_pdf", # Replace with your own username
    version="0.0.1",
    author="Isidro Arias",
    author_email="isidroariass@hotmail.es",
    description="This convert a software proyect to a pdf book",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/isidroas/code_to_pdf",
    project_urls={
        "Bug Tracker": "https://github.com/isidroas/code_to_pdf/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'pygments',
        'pdfkit',
        'PyPDF2', 
        'reportlab',
        'jinja2',
        'art',
    ],
    entry_points = {'console_scripts':['code_to_pdf=code_to_pdf.__main__:main']},
    include_package_data= True
)
