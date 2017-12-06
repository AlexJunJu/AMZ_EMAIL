
import time

from threading import Event

# Event()对象用于线程之间的通信，判断线程设置的信号标志，假则等待，真则进行
# 内置标志默认为FALSE
# set()方法可以设置对象内部的信号标志为真
# is_set()方法用来判断其内部信号标志的状态
exit = Event()

def main():
    from sshtunnel import SSHTunnelForwarder
    server =  SSHTunnelForwarder(
                                ('209.9.106.163', 22), #Remote server IP and SSH port
                                ssh_username = "root",
                                ssh_password = "maxsonic@123888",
                                ssh_pkey = "D:/Software/putty/db.ppk",
                                local_bind_address=('127.0.0.1', 5432),
                                remote_bind_address = ('52.40.239.158', 5432),#binde local host
                                )
    server.start()
    print("Remote server is connected through SSH_tunnel")

    #当Event对象的内部信号标志为假时，wait()方法一直等待到其为真时才返回
    #此时的is_set()为假
    #while语句的判断条件为真
    #wait()方法一直被阻塞
    while not exit.is_set():
       time.sleep(1)
       exit.wait(1)

    server.close()

# 信号处理函数
# 即通过通过一个回调函数来接收信号，会在信号出现时调用。
def quit(signo, _frame):
    print("Interrupted by %d, shutting down" % signo)
    # set()方法可以设置对象内部的信号标志为真
    exit.set()

if __name__ == '__main__':

    # signal，进程之间通讯的方式，是一种软件中断
    # 一个进程在在执行其原来的程序流程时，如果接收到signal,会打断其原来的只需顺序，来执行处理函数
    # SIGINT，终止进程、中断进程（control+C）信号
    import signal
    # signal.signal()函数来预设信号处理函数
    signal.signal(signal.SIGINT, quit)
    main()


