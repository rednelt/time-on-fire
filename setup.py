from setuptools import setup, find_packages

setup(
    name='time-on-fire',
    version='0.1.1',
    author="zapvolt",
    author_email="ag11012008@gmail.com",
    description="A simple activity tracker for Windows.",
    license="GNU GPLv3",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    packages=["time_on_fire"],
    package_data={
        "time_on_fire": ["activities.db"],
    },
    include_package_data=True,
    install_requires=[
        "click", "pywin32", "psutil", "tabulate"
    ],
    keywords=["python time-tracking time tracking monitoring report"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        "console_scripts": [
            "tof=time_on_fire.cli:cli",
        ],
    },
)
