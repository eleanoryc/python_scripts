#!/usr/bin/python

import logging
import sample_logging_2 

def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.info('Started')
    sample_logging_2.do_something()
    logging.info('Finished')

if __name__ == '__main__':
    main()


