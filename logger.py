import logging
import os
import time
import sys

logger = logging.getLogger()

CUR_DIR = os.path.expanduser("~") + '/Documents/salesforce/python_script'

def configureLogging(dirName,logLevel=logging.INFO):
    global logger
    #Check if we have write permission in this dir
    if not os.access(dirName, os.W_OK):
        dirName = "/tmp"
    logDir = dirName + "/log"
    if not os.path.exists(logDir):
        os.makedirs(logDir)

    logFile = "testlog_" + time.strftime("%Y%m%d")
    logging.basicConfig(
        filename=logDir + '/' + logFile,
        level=logLevel,
        format='[%(asctime)s] ' + str(os.getpid()) + ' %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S %Z',
    )
    handler = logging.StreamHandler()
    handler.setLevel(logLevel)
    logger.addHandler(handler)

    

def main():

    argv = sys.argv[1:]

    #Setup the logger utility
    configureLogging(CUR_DIR,logging.INFO)

    logger.info("-" * 100)
    logger.info('Executing: ' + str(sys.argv))
    logger.info("-" * 100)

    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")


    exit(0)

if __name__ == '__main__':
    main()


