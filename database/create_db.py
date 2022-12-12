from .schema import metadata
from app import main

import sys
sys.path.append("..")


if __name__ == "__main__":
    metadata.create_all(main.engine)
