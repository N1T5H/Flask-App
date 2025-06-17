from prometheus_client import Counter, generate_latest
from flask import Response

QUOTE_COUNTER = Counter('quotes_served_total', 'Total number of quotes served')

def metrics():
    return Response(generate_latest(), mimetype="text/plain")
