import os
import getopt
import sys
import logging

h_path = os.path.expanduser('~')
th_path = h_path + '/taghome'
#pri_path = th_path + '/test'
#log_path = prj_path + '/' + 'search.log'

def search_src(root, file, cpl):
    name_str = os.path.splitext(file)
    basename = name_str[0]
    baseneme = os.path.abspath(basename)
    extname = name_str[1]

    src_file = os.path.join(root,file)
    if extname in ['.h', '.H', '.lds']:
        logging.info("%s"%(src_file))
    if extname in ['.c', '.C', '.s', '.S', '.dts', '.dtsi']:
        if cpl:
            obj = basename + '.o'
            dtb = basename + '.dtb'
            obj_file = os.path.join(root,obj)
            dtb_file = os.path.join(root,dtb)
            if os.path.exists(obj_file) or os.path.exists(dtb_file):
                logging.info("%s"%(src_file))
        else:
            logging.info("%s"%(src_file))

def search_file(path, cpl):
    for root, dirs, files in os.walk(path, topdown=True):
        root = os.path.abspath(root)
        for file in files:
            search_src(root, file, cpl)
        for dir in dirs:
            search_file(dir, cpl)

def parse_dir(va):
    global prj_path, log_path
    prj_path = th_path + '/' + va
    log_path = prj_path + '/search.log'
    
    if os.path.exists(th_path):
        if os.path.exists(prj_path):
            if os.path.exists(log_path):
                os.remove(log_path)
                print("remove pre log file...")
            else:
                print("create new log file")
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

    os.chdir(prj_path)
    os.system("cscope -Rbq -i %s"%(log_path))
    os.system("ctags -L %s"%(log_path))
    
    sys.exit()
