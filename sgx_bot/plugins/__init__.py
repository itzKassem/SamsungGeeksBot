"""List All Plugins!"""
# Copyright (C) 2020 - 2020 KassemSYR. All rights reserved.
# This file is part of Galaxy Helper bot.

import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def __list_all_plugins():
    from os.path import dirname, basename, isfile
    import glob

    plugin_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [
        basename(f)[:-3]
        for f in plugin_paths
        if isfile(f)
        and f.endswith(".py")
        and not f.endswith("__init__.py")
        and not f.endswith("__help__.py")
    ]
    return all_modules


all_plugins = sorted(__list_all_plugins())
logger.info("loadded plugins: %s", str(all_plugins))
__all__ = all_plugins + ["all_plugins"]
