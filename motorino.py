import SimpleHTTPServer
import SocketServer
import pickle
import subprocess
import signal
import urlparse 
import json
import hashlib
import redis
import os
import imp

PORT    = 617

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_the_404(self):
        p = '<html><h1>ONORE AL COMMENDATORE</h1><audio autoplay loop><source src="http://www.fileden.com/files/2009/3/22/2374149/Giorgio%20Moroder%20-%20Einzelganger%20%281%29%20-%20Einzelganger.mp3" type="audio/mp3"></audio><p><img alt="" src="http://25.media.tumblr.com/tumblr_lxom7sxjDv1qcy8xgo1_500.gif" class="alignnone" width="500" height="333"></p></html>'
        self.send_response(404)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-length", str(len(p)))
        self.end_headers()
        self.wfile.write(p)
        self.wfile.flush()
        self.connection.shutdown(1)

    def do_the_dance(self):
        rinasci_arnaldo()

    def do_GET(self):
        self.do_the_404()

    def do_POST(self):
        if self.path != '/github':
            self.do_the_404()
            return

        length = int(self.headers['Content-Length'])
        post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))

        if post_data.has_key('payload') and len(post_data['payload']) > 0:
            payload = json.loads(post_data['payload'][0])
            commits = payload.get('commits', None)
            if commits != None and len(commits) > 0:
                url = '/'.join(commits[0].get('url', None).split('/')[:-2])
                print url
                author = commits[0].get('author', None).get('name', None)
                message = commits[0].get('message', None)
                print "<%s>: %s" % (author, message)
                    
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('ONORE AL COMMENDATORE')

        cwd = os.getcwd()
        os.chdir(roba[url])
        subprocess.check_call(['git', 'pull'])
        imp.load_source('motoraggio', '%s/motoraggio.py' % roba[url])
        import motoraggio
        motoraggio.smazza()
        del motoraggio
        os.chdir(cwd)

if __name__ == '__main__':
    roba    = None
    global roba

    print 'Starting arnaldo'
    mot = open('motorino.json', 'r')
    roba = json.load(mot)
    mot.close()

    print "Starting webserver (%s)" % (PORT,)
    httpd = SocketServer.TCPServer(("", PORT), ServerHandler)
    try:
        httpd.serve_forever()
    except Exception, KeyboardInterrupt:
        httpd.shutdown() 
