import subprocess
import os
import sys
import re
import gzip 

def get_filename(file, format, drop=False):
    if drop:
        return re.sub(rf'(_R1|_R2|_1|_2)?\.{format}(.gz)?$','',os.path.basename(file))
    else:
        return re.sub(rf'\.{format}(.gz)?$','',os.path.basename(file))
        
## https://stackoverflow.com/a/850962
def buffer_count(file, logger):
    nlines = 0
    if re.search('.gz$', file):
        f = gzip.open(file, 'rt')
    else:
        f = open(file)

    char = f.read(1) # get first character, > or @
    f.seek(0) # roll back

    buf_size = 1024 * 1024
    read_f = f.read
    
    buf = read_f(buf_size)
    while buf:
        nlines += buf.count('\n')
        buf = read_f(buf_size)

    f.close()
    if char == '>':
        return int(nlines/2)
    elif char =='@':
        return int(nlines/4)
    else:
        logger.critical('Unrecognized file format <{}>. Only fasta or fastq supported.'.format(file))
        sys.exit(2)

def simple_count(file):
    nbps = 0
    nlines = 0
    f = open(file)

    char = '>'
    record = False
    for line in f:
        if line[0] == char:
            nlines += 1
            record = True # record next row

        elif record:
            nbps += len(line) - 1
            record = False
            
    f.close()
    return nbps, nlines