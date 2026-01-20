import sys

from loguru import logger


class LogConfig:
    """   Configuration de logs pour le serveur.
    #
    #     Cette classe définit la configuration de logs à utiliser pour le serveur,
    #     incluant les filtres, les formatters, les handlers, et les loggers.
    #     """
    #
    # Nom du logger principal
    LOGGER_NAME: str = "main"
    # Format du log
    #LOG_FORMAT: str = "%(asctime)s - %(correlation_id)s - %(name)s - %(levelname)8s - (%(filename)10s:%(lineno)04d) - %(message)s"
    LOG_FORMAT: str = ("{time:YYYY-MM-DD HH:mm:ss} - {extra[workflow_id]} - {name} - {level: <8} - "
                       "({file: <10}:{line:04d}) - {message}")

    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    # Niveau de log par défaut
    LOG_LEVEL: str = "INFO"


# Format personnalisé avec contexte Temporal
def loguru_temporal_format(record):
   # record["extra"]["workflow_id"] = workflow_id or "-"
    return (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{extra[workflow_id]: <30}</cyan> | "
        "<cyan>{extra[activity_name]: <25}</cyan> | "
        "<cyan>{name: <50}</cyan>:<cyan>{function: <20}</cyan>:<cyan>{line: <4}</cyan> | "
        "<level>{message}</level>\n"
    )


def setup_logger():

    # Delete default configuration
    logger.remove()

    # Console output (coloré)
    logger.add(
        sys.stderr,
        format=loguru_temporal_format,
        level=LogConfig.LOG_LEVEL,
        colorize=True,
        backtrace=True,
        diagnose=True
    )

    # Default value bind for Temporal context
    logger.configure(extra={
        "workflow_id": "N/A",
        "activity_name": "N/A"
    })

    logger.info("Logger successfully configured")