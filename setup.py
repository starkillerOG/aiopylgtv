from setuptools import setup

with open("README.md") as f:
    readme = f.read()

setup(
    name="aiopylgtv",
    packages=["aiopylgtv"],
    install_requires=["websockets", "numpy"],
    python_requires=">=3.6",
    zip_safe=True,
    version="0.2.5",
    description="Library to control webOS based LG TV devices.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Josh Bendavid",
    author_email="joshbendavid@gmail.com",
    url="https://github.com/bendavid/aiopylgtv",
    download_url="https://github.com/bendavid/aiopylgtv/archive/0.2.5.tar.gz",
    keywords=["webos", "tv"],
    classifiers=[],
    entry_points={
        "console_scripts": ["aiopylgtvcommand=aiopylgtv.utils:aiopylgtvcommand"],
    },
)
