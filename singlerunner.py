#!/usr/bin/python
#coding: UTF-8

'''
SingleRunner makes sure only one instance of programme running at the same time.
the programme most likes:
    1. it would run very long or run forever in a loop
    2. and more running at the same time would make something terribly bad

so, use SingleRunner like this:

def mymain(count=5, fn="ztest.log"):
        import time, os
        pid = os.getpid()
        print 'pid[%s] to loop: %s' % (pid, count)
        fo = open(fn, 'w')
        i = 0
        while 1:
            i += 1
            if i > count:
                print 'bad:' , i/1
                break
            msg = 'pid[%s] sleeping: %s' % (pid, i)
            print msg
            fo.write(msg + '\n')
            fo.flush()
            time.sleep(1)
        print 'done, bye!'

    pm = SingleRunner(__file__)
    import sys
    as_daemon = False
    if len(sys.argv) == 2:
        if sys.argv[1] == 'daemon':
            as_daemon = True
    pm.run(as_daemon, mymain, 20, fn='abc')

'''
class SingleRunner(object):
    def __init__(self, file_name):
        import os, sys, signal, traceback
        self.os = os
        self.sys = sys
        self.signal = signal
        self.traceback = traceback
        self.RED = '\x1b[31m'
        self.GRE = '\x1b[32m'
        self.BRO = '\x1b[33m'
        self.BLU = '\x1b[34m'
        self.PUR = '\x1b[35m'
        self.CYA = '\x1b[36m'
        self.WHI = '\x1b[37m'
        self.NOR = '\x1b[0m'
        fn = self.os.path.basename(file_name)
        self.pidfile = '/tmp/%s.pid' % fn
        self.stop_reason = 'exit normally'
        self.check_running()
        #print '%screated pidfile: %s%s' % (self.GRE, self.pidfile, self.NOR)

    def termination_handler (self, signum,frame):
        print '\n%sYou have requested to terminate the application...%s' % (self.RED, self.NOR)
        self.sys.stdout.flush()
        self.stop_running('keyboard interrupt')
        raise KeyboardInterrupt()
        #sys.exit(-1)

    def check_running(self, ):
        if self.os.path.isfile(self.pidfile):
            print ("%spidfile: %s %salready exists, exiting...\n"
                   'To run this programme, you should:\n'
                   '\t1. make sure there is no instance running, \n'
                   '\t2. then remove the pidfile: %s%s%s') % (
                       self.GRE,
                       self.pidfile,
                       self.BRO,
                       self.GRE,
                       self.pidfile,
                       self.NOR)
            self.sys.exit()
        else:
            self.signal.signal(self.signal.SIGINT,self.termination_handler)
            self.signal.signal(self.signal.SIGTERM,self.termination_handler)
            self.signal.signal(self.signal.SIGSEGV,self.termination_handler)
            file(self.pidfile, 'w').write('1')

    def stop_running(self, msg='normally'):
        if self.os.path.isfile(self.pidfile):
            print '\n%sstop_running with reason: %s"%s"%s\n' % (
                self.GRE,
                self.BRO,
                msg,
                self.NOR
            )
            self.os.unlink(self.pidfile)
    def run_normally(self, func, *args, **kwargs):
        print 'start running...'
        self.check_running()
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            self.stop_reason = 'keyboard interrupt'
        except:
            self.traceback.print_exc()
            self.stop_reason = 'Exception'
        self.stop_running()

    def run_as_daemon(self, func, *args, **kwargs):
        import daemon, signal
        self.check_running()
        context = daemon.DaemonContext(
            working_directory = '/tmp'#self.os.getcwd(),
        )
        context.signal_map = {
            signal.SIGTERM: self.termination_handler,
        }
        print 'start running as daemon ...'
        with context:
            func(*args, **kwargs)
            self.stop_running()

    def run(self, as_daemon, func, *args, **kwargs):
        if as_daemon:
            self.run_as_daemon(func, *args, **kwargs)
        else:
            self.run_normally(func, *args, **kwargs)

if __name__ == '__main__':
    def mymain(count=5, fn="ztest.log"):
        import time, os
        pid = os.getpid()
        print 'pid[%s] to loop: %s' % (pid, count)
        fo = open(fn, 'w')
        i = 0
        while 1:
            i += 1
            if i > count:
                print 'bad:' , i/1
                break
            msg = 'pid[%s] sleeping: %s' % (pid, i)
            print msg
            fo.write(msg + '\n')
            fo.flush()
            time.sleep(1)
        print 'done, bye!'

    pm = SingleRunner(__file__)
    import sys
    as_daemon = False
    if len(sys.argv) == 2:
        if sys.argv[1] == 'daemon':
            as_daemon = True
    pm.run(as_daemon, mymain, 20, fn='abc')

