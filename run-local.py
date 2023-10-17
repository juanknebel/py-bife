#!/usr/bin/env python
import uvicorn
from py_bife import my_config


def start():
    uvicorn.run(
        "py_bife:create_app",
        reload=True,
        workers=my_config.WORKERS,
        host=my_config.HOST,
        port=my_config.PORT,
        log_level=my_config.LOG_LEVEL,
    )


if __name__ == "__main__":
    start()
