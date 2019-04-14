import ure
from filehelper import makefileifneed
import ujson
from machine import reset

import time
import os
import usocket as socket


class websettings:

    def __init__(self):
        self.config_name = 'config.json'
        self.tempvars = {}
        self.regex = ''
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', 80))
        self.s.listen(1)
        self.s.settimeout(10)
        # self.s.setblocking(False)



    def optionmaker(self, options, name):
        optionlist = '<select name="' + name + '">'
        
        for optname in options:
            uppercase = optname[0].upper() + optname[1:]
            optionlist += '<option value="' + optname + '">' + uppercase + '</option>'

        optionlist += '</select>'

        return optionlist


    def clear_settings(self):
        os.remove(self.config_name)


    def test_config(self):
        existing_config = None
        try:
            f = makefileifneed(self.config_name)
            existing_config = f.read()

            existing_config = ujson.loads(existing_config)
            f.close()
            
        except Exception as e:
            print("No saved network:", e)
            f.close()
        return existing_config

    def setregexp(self, listogerexps):
        self.formitems = listogerexps
        regstr = ''
        for regitem in listogerexps:
            regstr += regitem +'=(.*?)&'
        regstr =regstr[:-1]
        print(regstr)
        regstr = 'network\?' + regstr + "\sHTTP"
        self.regex = ure.compile(regstr)

    def getformvalues(self, result):
        formkeyvals = {}
        for fitem in self.formitems:
            formkeyvals.update({fitem:result.group(self.formitems.index(fitem)+1)})
        return formkeyvals

    def generate_html(self):
        if self.tempvars:
            return self.template.format(**self.tempvars).replace('[','{').replace(']','}')
        return self.template.replace('[','{').replace(']','}')

    def generate_reaction_good(self):
        return "<!doctype html> All good, good reaction wait for a while, will reset !"


    def generate_reaction_bad(self):
        return "<!doctype html> All bad wait a while but in general fuck u"


    def addTempVars(self, adict):
        self.tempvars.update(adict)

    def write_html(self,client_stream, html):
        client_stream.write("HTTP/1.0 200 OK\nContent-Type: text/html\n\n" + html)

    def setTemplate(self, filename):
        self.template = makefileifneed(filename).read()
        if not self.template:
            self.template = "No template found !"

    def setConfigName(self, configname):
        self.configname = configname

    def WEBQnA(self):
        
        try:
            res = self.s.accept()
            client_sock = res[0]
            client_addr = res[1]

            req = client_sock.readline()
            while True:
                h = client_sock.readline()
                if h == b"" or h == b"\r\n" or h == None:
                    break

            if self.handle_form(req):
                self.write_html(client_sock, self.generate_reaction_good())
                # time.sleep(0.5)
                reset()
            else:
                self.write_html(client_sock, self.generate_html())

            client_sock.close()
            
        except Exception as e:
            print("timeout for web... moving on...", e)
 

    def handle_form(self, data):
        search_result = self.regex.search(data)
        if search_result:
            f = makefileifneed(self.config_name)
            f.write(ujson.dumps(self.getformvalues(search_result)))
            f.close()
            return True
        return False
