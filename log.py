import logging
# added log file to debug and track the pipeline execution
# Set up logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("run_pipeline.log", mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def log_print(*args, **kwargs):
    message = ' '.join(str(a) for a in args)
    logging.info(message)
