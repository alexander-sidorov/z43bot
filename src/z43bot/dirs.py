from pathlib import Path

_this_file = Path(__file__).resolve()

DIR_BOT_PACKAGE = _this_file.parent
DIR_SRC = DIR_BOT_PACKAGE.parent
DIR_TEMPLATES = DIR_SRC / "templates"
