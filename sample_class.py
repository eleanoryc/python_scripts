import os
import socket
import re

class hostsfdc():
    def instance(self):
        return socket.gethostname().split('-')[0]

    def role(self):
        part = re.sub(r'\d', "", socket.gethostname().split('-')[1])
        return part

    def group(self):
        part = re.sub(r'\D', "", socket.gethostname().split('-')[1])
        return part

    def node(self):
        part = socket.gethostname().split('-')[2]
        return part

    def site(self):
        part = socket.gethostname().split('-')[3].split('.')[0]
        return part

    def domain(self):
        part = re.sub(r'^[a-z]+.', '', socket.gethostname().split('-')[3])
        return part


# how to call and assign to a variable
sitecode = hostsfdc()
print type(sitecode)

site = sitecode.site()
print type(site)

