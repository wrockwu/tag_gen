import os
import getopt
import sys
import logging


def search_src(root, file, cpl):
    name_str = os.path.splitext(file)
    basename = name_str[0]
    baseneme = os.path.abspath(basename)
    extname = name_str[1]
    if extname in ['.c', '.C', '.s', '.S']:
        src_file = os.path.join(root,file)
        
        if cpl:
            logging.info("%s" %(src_file))
        else:
            obj = basename + '.o'
            obj_file = os.path.join(root,obj)

            if os.path.exists(obj_file):
                logging.info("%s" %(src_file))

def search_file(path, cpl):
    for root, dirs, files in os.walk(path, topdown=True):
        for file in files:
            search_src(root, file, cpl)
        for dir in dirs:
            search_file(dir, cpl)

def parse_dir(va):
    h_path = os.path.expanduser('~')
    th_path = h_path + '/taghome' 
    prj_path = th_path + '/' + va
    
    if os.path.exists(th_path):
        if os.path.exists(prj_path):
            print("use pre fold...")
        else:
            try:
                os.mkdir(prj_path)
            except Exception as err:
                print("mkdir prj fold failed...")
                return False
    else:
        try:
            os.mkdir(th_path)
            os.mkdir(prj_path) 
        except Exception as err:
            print("create fold failed...")
            return False

    log_path = prj_path + '/' + 'search.log' 
    logging.basicConfig(level=logging.DEBUG, format='', filename=log_path, filemode='a')
    return True

def help_msg():
    print("Command Usage: python3 rmidlsrc -d [dir] -p [src path]")

if __name__=='__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'chd:p:', ['--cplile'])
    except Exception as err:
        print("Command failed:%s" %err)
        help_msg()
        print("Detail message as bellow:")
        sys.exit(2)
    
    if not opts:
        help_msg()
        exit(0)
    
    prj_path_res = False
    cpl = False
    src_path = []
    for op, va in opts:
        if op in ['-p', '--path']:
            src_path.append(va)
            for arg in args:
                src_path.append(va)
        elif op in ['-h', '--help']:
            help_msg()
            sys.exit()
        elif op in ['-c', '--cplile']:
            cpl = True
        elif op in ['-d', '--dir']:
            prj_path_res = parse_dir(va)
    
    for p in src_path :
        search_file(p, cpl)

    sys.exit()