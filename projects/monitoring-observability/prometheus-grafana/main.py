from prometheus_client import start_http_server, Counter, Summary, Histogram
import random
import time

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    print(t)
    time.sleep(t)

def historgram():
    h = Histogram('request_latency_seconds', 'Description of histogram')
    h.observe(4.7)    # Observe 4.7 (seconds in this case)

def counter():
    c = Counter('my_requests_total', 'HTTP Failures', ['method', 'endpoint'])
    c.labels('get', '/').inc()
    c.labels('post', '/submit').inc()


if __name__ == '__main__':
    start_http_server(8000) # Start up the server to expose the metrics.
    historgram()
    counter()
    while True: # Generate some requests.
        process_request(random.random())
        
        