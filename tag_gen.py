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
    extname = name_str[1]

    src_file = os.path.join(root,file)
    if extname in ['.h', '.H', '.lds']:
        logging.info("%s"%(src_file))
    elif extname in ['.c', '.C', '.s', '.S', '.dts', '.dtsi']:
        if cpl:
            obj = basename + '.o'
            dtb = basename + '.dtb'
            obj_file = os.path.join(root,obj)
            dtb_file = os.path.join(root,dtb)
            if os.path.exists(obj_file) or os.path.exists(dtb_file):
                print("add file:%s"%(src_file))
                logging.info("%s"%(src_file))
        else:
            print("add file:%s"%(src_file))
            logging.info("%s"%(src_file))

def search_file(path, cpl):
    for root, dirs, files in os.walk(path, topdown=True):
        if "/." in root:
            #ignore dir as '.git' '.vim'
            continue
        root = os.path.abspath(root)
        for file in files:
            if file.startswith("."):
                #ignore file start with '.', such as '.config' '.build-in.o.cmd'
                continue
            search_src(root, file, cpl)

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
    print("Command Usage: python3 rmidlsrc -p [tag path] -d [src dir]")

if __name__=='__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'chka:d:p:', ['--arch=', '--compile', '--dir=', '--path=', '--help' ])
    except Exception as err:
        print("Command failed:%s" %err)
        help_msg()
        print("Detail message as bellow:")
        sys.exit(2)
    
    if not opts:
        help_msg()
        exit(0)
    
    arch = None
    kernel = False
    prj_path_res = False
    cpl = False
    src_path = []
    for op, va in opts:
        if op in ['-a', '--arch']:
            arch = va
        elif op in ['-k', '--kernel']:
            kernel = True
        elif op in ['-p', '--path']:
            prj_path_res = parse_dir(va)
        elif op in ['-h', '--help']:
            help_msg()
            sys.exit()
        elif op in ['-c', '--compile']:
            cpl = True
        elif op in ['-d', '--dir']:
            src_path.append(va)
            for arg in args:
                src_path.append(va)

    
    for p in src_path:
        search_file(p, cpl)

    if kernel is True:
        path = os.path.abspath(src_path[0])
        if path.endswith('/'):
            arch_root = path + 'arch/'
            arch_path = arch_root + str(arch)
        else:
            arch_root = path + '/arch/'
            arch_path = arch_root + str(arch)

    os.chdir(prj_path)

    cscope_log = prj_path + '/cscope.log'
    with open(log_path) as f:
        with open(cscope_log, 'w') as wf:
            for line in f.readlines():
                if arch_root in line:
                    if arch_path in line:
                        wf.write(line)
                    else:
                        continue
                else:
                    wf.write(line)

    os.system("cscope -Rbq -i %s"%(cscope_log))
    os.system("ctags -L %s"%(cscope_log))
    
    sys.exit()
