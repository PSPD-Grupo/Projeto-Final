from prometheus_client import Counter, Histogram, start_http_server

TRANSFORM_REQUESTS = Counter(
    "datatransform_requests_total", "Total de transformações", ["access_level", "rpc"]
)
TRANSFORM_ERRORS = Counter(
    "datatransform_errors_total", "Total de erros", ["error_type"]
)
TRANSFORM_LATENCY = Histogram(
    "datatransform_latency_seconds", "Latência da transformação", ["rpc"]
)

def start_metrics_server(port: int):
    start_http_server(port)