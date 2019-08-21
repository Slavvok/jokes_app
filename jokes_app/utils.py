import logging

logger = logging.getLogger('visit_log')
logger.setLevel(logging.INFO)


def logging(req, user_id=None):
    path = req.path
    user_id = req.user.id
    ip = req.META['REMOTE_ADDR']
    logger.info(f"{path} {user_id} {ip}")
