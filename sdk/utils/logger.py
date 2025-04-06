import logging
from typing import Optional

def get_logger(name: str, level: int = logging.INFO, formatter: Optional[logging.Formatter] = None) -> logging.Logger:
  """
  Return a logger instance with a give name and logging level.
  If no formatter is provided, a default formatter will be used.
  """
  logger = logging.getLogger(name)
  logger.setLevel(level)

  if not logger.handlers:
    # create a console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # use a default formatter if none is provided
    if formatter is None:
      formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
      )
    ch.setFormatter(formatter)

    # add the handler to the logger
    logger.addHandler(ch)

  return logger