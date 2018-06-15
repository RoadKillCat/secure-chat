import http.server
import socketserver
import random,json,hashlib,os,signal,sys
import threading

PORT = 8000
fdata = 'data.json'
findex = 'index.html'
std_cols = ['#f00','#0f0','#00f']

try:
    with open(fdata) as f:
        data = json.loads(f.read())
except FileNotFoundError:
    data = {'users': {}, 'messages': []}

num_msgs = len(data['messages'])

class Handler(http.server.BaseHTTPRequestHandler):
    def get_uid(self):
        #returns a unique string based on their ip
        self.ip  = self.client_address[0]
        self.uid = hashlib.sha1(self.ip.encode('utf-8')).hexdigest()[:6]
        if self.uid not in data['users']:
            print(self.uid, 'is new')
            try:
                data['users'][self.uid] = {'color': next(c for c in std_cols if not any(c==v['color'] for v in data['users'].values()))}
            except StopIteration:
                print('no new colours, assigning purple')
                data['users'][self.uid] = {'color': '#f0f'}

    def do_GET(self):
        self.get_uid()
        path = self.path

        if path == '/new_messages':
            #(hanging GET)
            #compares the number of messages they have to the actual
            #enters infinite loop whilst there are no new messages
            tnm = int(self.headers['num_msgs'])
            while tnm == num_msgs:
                pass
            body = json.dumps(data).encode('utf-8')
            ctype = 'text/plain'
        else:
            print(self.uid, 'joined')
            #get all files
            fs = [f for f in os.listdir() if f in path]
            #if no file in dir, default to index.html
            f  = fs[0] if len(fs) else findex
            #open file in read binary mode and read
            with open(f, 'rb') as fh:
                body = fh.read()
            ctype = 'text/html' if f==findex else 'text/plain'

        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        global num_msgs
        num_msgs += 1

        self.get_uid()

        clen = int(self.headers['Content-Length'])
        msg = self.rfile.read(clen).decode('utf-8')

        data['messages'].append({'uid':self.uid, 'text':msg})

        self.send_response(200)
        self.end_headers()

    #stop BaseHTTPRequestHandler outputting
    def log_message(self, format, *args):
        return

#saves the data to the json file
def save_data(*args):
    print('\rclosing...\nsaving messges to {}...'.format(fdata))
    with open(fdata,'w') as f:
        f.write(json.dumps(data))

    print('save successful')
    sys.exit()

#handle any method of killing the server
sigs = set(signal.Signals) - {signal.SIGKILL,signal.SIGSTOP}
for s in sigs:
    signal.signal(s, save_data)

#serve
print('Serving at port', PORT)

socketserver.TCPServer.allow_reuse_address=1
server = socketserver.ThreadingTCPServer(('',PORT), Handler)
server.serve_forever()
server.shutdown()
server.server_close()
