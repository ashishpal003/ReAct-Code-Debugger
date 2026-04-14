"""
Maps import names to pip-installable package names.
"""

IMPORT_TO_PACKAGE_MAP = {
    "sklearn": "scikit-learn",
    "cv2": "opencv-python",
    "PIL": "pillow",
    "yaml": "pyyaml",
    "bs4": "beautifulsoup4",
    "dotenv": "python-dotenv",
    "langchain": "langchain",
    "pandas": "pandas",
    "numpy": "numpy",
}


def map_import_to_package(import_name: str) -> str:
    """Return the correct pip package name."""
    return IMPORT_TO_PACKAGE_MAP.get(import_name, import_name)