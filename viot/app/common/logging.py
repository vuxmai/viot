import logging as std_logging


def setup_logging() -> None:
    level = std_logging.DEBUG

    console_handler = std_logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(ColorizedFormatter())
    std_logging.basicConfig(level=level, handlers=[console_handler])

    # Disable when in production
    std_logging.getLogger("sqlalchemy.engine").setLevel(std_logging.INFO)


class ColorizedFormatter(std_logging.Formatter):
    """std_logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    bold = "\x1b[1m"
    grey = f"{bold}\x1b[38;21m"
    blue = f"{bold}\x1b[38;5;39m"
    yellow = f"{bold}\x1b[38;5;229m"
    red = f"{bold}\x1b[38;5;203m"
    bold_red = f"{bold}\x1b[31;1m"

    def __init__(self, fmt: str | None = None) -> None:
        super().__init__()
        # Loguru color style
        self.fmt = fmt or (
            "\x1b[32m%(asctime)s\x1b[0m | "
            "%(levelname)-8s\x1b[0m | "
            "\x1b[36m%(name)s\x1b[0m:\x1b[36m%(funcName)s\x1b[0m:\x1b[36m%(lineno)d\x1b[0m"
            " - %(message)s\x1b[0m"
        )
        self.FORMATS = {
            std_logging.DEBUG: self.blue,
            std_logging.INFO: self.grey,
            std_logging.WARNING: self.yellow,
            std_logging.ERROR: self.red,
            std_logging.CRITICAL: self.bold_red,
        }

    def format(self, record: std_logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        if not log_fmt:
            return super().format(record)
        formatter = std_logging.Formatter(self.fmt)
        record.levelname = log_fmt + record.levelname
        record.msg = log_fmt + str(record.msg)
        return formatter.format(record)
