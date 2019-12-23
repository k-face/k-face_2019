from config import configuration
from worker import worker

config = configuration()
work = worker(config)
work.train(config)