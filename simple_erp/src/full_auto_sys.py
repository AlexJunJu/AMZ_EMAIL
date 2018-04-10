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
		
		




def auto_ssh_erp_email():
	ssh_tunnel = SshTunnel()
	ssh = ssh_tunnel.get_ssh()
	ssh.start()
	time.sleep(5)
	try:
		from erp_helper import erp_helper
		from mail import mail_sending_system
		erp_helper()
		mail_sending_system()
	except Exception as e:
		raise
	else:
		print("All jobs is done!")
	finally:
		ssh.close()


if __name__ == '__main__':
	#auto_ssh_erp_email()
	do_main()