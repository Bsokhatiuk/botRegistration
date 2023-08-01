import datetime
import logging
from flask import request
class ContextualFilter(logging.Filter):
    def filter(self, log_record):
        ''' Provide some extra variables to give our logs some better info '''
        log_record.utcnow = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S,%f %Z')
        log_record.url = request.path
        log_record.method = request.method
        # Try to get the IP address of the user through reverse proxy
        log_record.ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        return True