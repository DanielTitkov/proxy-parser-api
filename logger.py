import sys
from loguru import logger

logger.configure(
    handlers=[
        dict(
            sink=sys.stdout, 
            level='INFO', 
            format="[{time}] [{name}] [{level}] {message}"
        ),
    ]
)