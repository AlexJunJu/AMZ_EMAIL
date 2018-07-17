#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
from utils import SshTunnel

def ssh_generator():
	ssh_tunnel = SshTunnel()
	ssh = ssh_tunnel.get_ssh()
	return ssh

def main():
	try:
		from erp_helper import erp_helper
		from mail import mail_sending_system
		erp_helper()
		mail_sending_system()
	except Exception as e:
		return False
	else:
		return True

def do_main():
	while not main():
		ssh = ssh_generator()
		ssh.start()
		time.sleep(5)
		try:
			main()
		except Exception as e:
			pass
		else:
			ssh.close()
			return True
		finally:
			ssh.close()
	print("All jobs is done!")
		
<<<<<<< HEAD
=======
		

>>>>>>> ea1f2b1c1d5258298be1420381d67e8cb003c069

if __name__ == '__main__':
	do_main()