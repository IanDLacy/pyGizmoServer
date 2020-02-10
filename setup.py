from setuptools import setup

setup(
    name="pyGizmoServer",
    version="1.0.2",
    python_requires=">=3.7",
    packages=[
        "TestCube",
        "MockUSB",
        "pyGizmoServer",
        "TestCube.TestCubeComponents",
        "tests",
        "static",
    ],
    install_requires=[
        "jsonpatch",
        "dpath",
        "websockets",
        "aiohttp",
        "aiojobs",
        "jinja2",
        "aiohttp-jinja2",
        "pyusb",
        "pytest",
        "app-settings",
    ],
    package_data={"schemas": ["*.txt", "*.json"], "": ["*.md"]},
    entry_points={"console_scripts": ["gizmo=pyGizmoServer.run:main"]},
)
