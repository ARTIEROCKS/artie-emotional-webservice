bind = "0.0.0.0:5000"
workers = 1

def on_starting(server):
    from app import queue_service
    queue_service.start_consuming()
