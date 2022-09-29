from loguru import logger


logger.level("GEE", no=41, color="<red>")
logger.add("client.log",format="{time} [{level}] {name}:{module}:[{file}:{line}] {message} | {exception} ", rotation="500 MB",level='WARNING') 
logger.add("log.log",format="{time} [{level}] {name}:{module}:[{file}:{line}] {message} | ", rotation="500 MB")