#!/usr/bin/env python

"""Mail list cleaner
Usage:
  photo_processor.py [-l | --to-lower] [-o | --optimize] [-r | --recursive] (DIR ...)
  photo_processor.py (-h | --help)
  photo_processor.py (-v | --version)

Options:
  -h --help       show this screen.
  -v --version    show version.
  -l --to-lower   change all names to lower case
"""
import logging
from os import rename, walk as walkFiles
from os.path import join as pathJoin, splitext
from docopt import docopt

def renameFile(root, oldName, newName):
    oldPath = pathJoin(root, oldName)
    newPath = pathJoin(root, newName)
    logging.debug('renaming file {0} to {1}'.format(oldPath, newPath))
    rename(oldPath, newPath)

class PathWalker:
    def __init__(self, dir, actions = None):
        self.dir = dir
        if actions is None:
            raise ValueError('Actions can not be None')
        self.actions = actions
    
    def walk(self, recursive = False):
        logging.info('walking dir {0}'.format(self.dir))
        for root, dirnames, filenames in walkFiles(self.dir):
            logging.debug('checking dir path: {0}'.format(root))
            self.processFiles(root, filenames)
        logging.debug('recursive option is: {0}'.format(recursive))
        if recursive:
            for dirname in dirnames:
                self.walk(dirname, recursive)
    
    def processFiles(self, root, filenames):
        for filename in filenames:
            base, ext = splitext(filename.lower())
            if ext != '.jpg' and ext != '.jpeg':
                logging.debug('ignoring non JPEG file {0}'.format(filename))
                continue
            logging.debug('procesing file {0}'.format(filename))
            self.actions.apply(root, filename)

class FileActionCollection:
    def __init__(self):
        self.actions = []
    def addAction(self, action):
        self.actions.append(action)
    def apply(self, root, filename):
        for action in self.actions:
            filename = action(root, filename)

class LowerCaseAction:
    def __call__(self, root, filename):
        oldName = filename
        newName = filename.lower()
        if oldName != newName:
            renameFile(root, oldName, newName)
            filename = newName
        return filename

class ExtNormalizerAction:
    def __call__(self, root, filename):
        base, ext = splitext(filename)
        if ext.lower() == '.jpeg':
            newName = base + '.jpg'
            renameFile(root, filename, newName)
            filename = newName
        return filename

class JpegOptimAction:
    def __call__(self, root, filename):
        from subprocess import Popen, PIPE
        f = pathJoin(root, filename)
        command = 'jpegoptim --preserve --verbose {0}'.format(f)
        p = Popen(command, shell=True, stdout = PIPE, stderr=PIPE)
        logging.debug('starting jpegoptim process')
        while p.poll() is None:
            out = p.stderr.read()
            err = p.stdout.read()
            if out != '':
                logging.debug(out)
            if err != '':
                logging.error(err)
        logging.debug('jpegoptim process finished')
        return filename

if __name__ == '__main__':
    logging.basicConfig(
        filename='photo_processor.log',
        level=logging.DEBUG,
        filemode='w'
    )
    logging.info('Started')

    arguments = docopt(__doc__, version='Images processor 1.0')

    fileActions = FileActionCollection()
    if arguments['--to-lower']:
        fileActions.addAction(LowerCaseAction())
    if arguments['--optimize']:
        fileActions.addAction(ExtNormalizerAction())
    fileActions.addAction(JpegOptimAction())

    for dir in arguments['DIR']:
        walker = PathWalker(dir, fileActions)
        walker.walk(arguments['--recursive'])
    
    logging.info('Finished')

