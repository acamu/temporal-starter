import inspect

from loguru import logger
from temporalio import workflow
from temporalio import activity
from typing import Optional


def get_workflow_logger(workflow_id: Optional[str] = None):
    """
    Retourne un logger avec le contexte workflows
    Le workflow_id est automatiquement détecté si non fourni
    """
    if workflow_id is None:
        try:
            workflow_id = workflow.info().workflow_id
        except:
            # Récupérer le nom de la fonction/classe appelante
            frame = inspect.currentframe()
            if frame and frame.f_back:
                workflow_id = frame.f_back.f_code.co_name
            else:
                workflow_id = "unknown"

    return logger.bind(
        workflow_id=workflow_id,
        activity_name="workflows"
    )

def get_activity_logger(activity_name: Optional[str] = None):
    """
    Retourne un logger avec le contexte activity
    Le nom de l'activité est automatiquement détecté si non fourni
    """
    if activity_name is None:
        try:
            # Essayer d'abord de récupérer depuis Temporal
            activity_name = activity.info().activity_type
        except:
            # Sinon, récupérer le nom de la fonction appelante
            frame = inspect.currentframe()
            if frame and frame.f_back:
                activity_name = frame.f_back.f_code.co_name
            else:
                activity_name = "unknown"

    workflow_id = "N/A"
    try:
        workflow_id = activity.info().workflow_id
    except:
        pass

    return logger.bind(
        workflow_id=workflow_id,
        activity_name=activity_name
    )


def get_logger(context: Optional[str] = None):
    """
    Retourne un logger générique avec contexte automatique
    Utilisé pour les services, utils, workers, etc.

    Args:
        context: Contexte optionnel (ex: "DatabaseService", "Worker", etc.)
                 Si non fourni, utilise le nom de la fonction/classe appelante

    Exemple:
        # Dans un service
        svc_logger = get_logger("PaymentService")

        # Détection automatique
        def process_data():
            log = get_logger()  # Contexte = "process_data"
            log.info("Processing...")
    """
    if context is None:
        # Récupérer automatiquement le contexte depuis la fonction appelante
        frame = inspect.currentframe()
        if frame and frame.f_back:
            # Essayer d'obtenir le nom de la classe si disponible
            caller_locals = frame.f_back.f_locals
            if 'self' in caller_locals:
                context = caller_locals['self'].__class__.__name__
            elif 'cls' in caller_locals:
                context = caller_locals['cls'].__name__
            else:
                # Sinon utiliser le nom de la fonction
                context = frame.f_back.f_code.co_name
        else:
            context = "worker"

    return logger.bind(
        workflow_id="N/A",
        activity_name=context
    )