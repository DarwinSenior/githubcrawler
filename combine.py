#!/usr/bin/env python

'''
This is a commandline utility function,
it combines the files under the directory(first argument)
and it combines from (second arguement default 1) certain file
to certain file (third arguement, default util file does not exists) 
'''

import argparse
import os, sys

def writeLine(fin, fout):
    for line in fin:
        fout.write(line)
    fout.write('\n')

def combiner(path, ffrom, fto, inputname, outputname):
    fto += 1    
    fout = open('%s/%s'%(path, outputname), 'w')
    i = ffrom
    inputnamei = inputname.replace('*', str(i))
    while i!=fto and os.path.isfile('%s/%s'%(path, inputnamei)):
        fin = open('%s/%s'%(path, inputnamei), 'r')
        writeLine(fin, fout)
        fin.close()
        i += 1
        inputnamei = inputname.replace('*', str(i))

    fout.close()
    print('Compressed file from %s to %s'%(ffrom, str(i-1)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Combine files numbered together")
    parser.add_argument('--path', dest='path', default='./data')
    parser.add_argument('--from', dest='ffrom', default=1)
    parser.add_argument('--to', dest='fto', default=-1)
    parser.add_argument('--input_name', dest='inputname', default='page_*.txt')
    parser.add_argument('--output_name', dest='outputname', default='pages.txt')
    args = parser.parse_args()
    path = os.path.abspath(args.path)
    outputname = args.outputname
    inputname = args.inputname
    ffrom = int(args.ffrom)
    fto = int(args.fto)

    combiner(path, ffrom, fto, inputname, outputname)



