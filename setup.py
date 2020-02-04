from setuptools import setup

setup(
    name="pyGizmoServer",
    version="1.0.1",
    python_requires=">=3.7",
    packages=[
        "controllers",
        "pyGizmoServer",
        "schemas",
        "controllers.TestCubeComponents",
        "tests",
        "static"
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
        "app-settings"
    ],
    package_data={"schemas": ["*.txt", "*.json"], "": ["*.md"]},
    entry_points={
        "console_scripts": [
            "gizmo=pyGizmoServer.run:main"
        ]
    },
)