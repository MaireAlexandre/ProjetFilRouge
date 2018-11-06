import os
from flask import Flask, flash, session, redirect, url_for, escape, request, render_template, json
from werkzeug.utils import secure_filename
import networkx as nx
import matplotlib.pyplot as plt
import hashlib as hasher
import datetime as date
import commands as cmds

UPLOAD_FOLDER = 'uploadFiles/'
ALLOWED_EXTENSIONS = set(['gml'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.errorhandler(404)
def ma_page_404(error):
    return render_template('404.html'), 404

@app.route('/')
@app.route('/index')
def index():
	if 'username' in session:
		return render_template('appgml.html')
	else:
		return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login(error=None):
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != '123':
            error = 'Invalid Login/Mot de passe'
        else:
            session['username'] = request.form['username']
            return redirect(url_for('appgml'))

    return render_template('login.html',error=error)


@app.route('/appgml', methods=['GET', 'POST'])
def appgml(error=None):
    if request.method == 'POST':
        listIP = getIP()
        if 'file' not in request.files:
            if 'newNode' in request.form:
                nodes = add_this_node(request.form["nodename"],request.form["nodeip"])
                edges = get_edges(UPLOAD_FOLDER+"up.gml")
                test = json.dumps(test_nodes(UPLOAD_FOLDER+"up.gml"))
                return render_template('appgml.html',error=error,nodes=nodes,edges=edges,nodesIP=test)
            elif 'newIOFile' in request.form:
                nodes = create_new_node()
                edges = get_edges(UPLOAD_FOLDER+"up.gml")
                return render_template('appgml.html',error=error)
            elif 'deleteNode' in request.form:
                nodes = remove_this_node(request.form["nodeD"])
                edges = get_edges(UPLOAD_FOLDER+"up.gml")
                return render_template('appgml.html',error=error,nodes=nodes,edges=edges)
            elif 'linknode' in request.form:
                nodes,result = add_egde(request.form["node1"],request.form["node2"])
                edges = get_edges(UPLOAD_FOLDER+"up.gml")
                return render_template('appgml.html',error=error,nodes=nodes,edges=edges,result=result)
            elif 'Deployer' in request.form:
                callSendIPConf()
                nodes = get_nodes(UPLOAD_FOLDER+"up.gml")
                edges = get_edges(UPLOAD_FOLDER+"up.gml")
                return render_template('appgml.html',error=error,nodes=nodes,edges=edges)
            else:
                return redirect(url_for('appgml',error='no in request file'))

        file = request.files['file']
        if file.filename == '':
            return redirect(url_for('appgml',error='no selected file'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = "up.gml"
	    status,output = cmds.getstatusoutput("python network/batch/clearpiconf.batch.py")
            laucheIP()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            attributeIP(listIP)
            test = get_nodes(UPLOAD_FOLDER+"up.gml")
            test2 = get_edges(UPLOAD_FOLDER+"up.gml")
            return render_template('appgml.html',error=error,nodes=test,edges=test2)

    else:
        return render_template('appgml.html',error=error)

def create_new_node():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    test = open(UPLOAD_FOLDER+"up.gml", 'w').close()
    G = nx.Graph()
    nx.write_gml(G,UPLOAD_FOLDER+"up.gml")



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def graph_gml(Path):
		Path_Png = UPLOAD_FOLDER+"/upImg.png"
		graphNetworkx = nx.read_gml(Path)
		nx.draw(graphNetworkx)
		plt.savefig(Path_Png)
		return Path_Png

def get_nodes(Path):
    gnx = nx.read_gml(Path)
    return (gnx.nodes())

def test_nodes(Path):
    gnx = nx.read_gml(Path)
    return( nx.get_node_attributes(gnx,'ip'))

def get_edges(Path):
    gnx = nx.read_gml(Path)
    return (gnx.edges())

def get_this_edge(node,edges):
    result = ""
    cpt= 0
    for edge in edges(node):
        cpt += 1
        result += edge[1]
        if (cpt < len(edges(node))):
            result+=" / "
    return(result)

def remove_this_node(node):
    gnx = nx.read_gml(UPLOAD_FOLDER+"up.gml")
    gnx.remove_node(node)
    nx.write_gml(gnx,UPLOAD_FOLDER+"up.gml")
    return (gnx.nodes())

def add_this_node(node,ip):
    gnx = nx.read_gml(UPLOAD_FOLDER+"up.gml")
    gnx.add_node(node,ip=ip)
    nx.write_gml(gnx,UPLOAD_FOLDER+"up.gml")
    return (gnx.nodes())

def add_egde(nodeSource,nodeDest):
    gnx = nx.read_gml(UPLOAD_FOLDER+"up.gml")
    test = gnx.add_edge(nodeSource,nodeDest)
    nx.write_gml(gnx,UPLOAD_FOLDER+"up.gml")
    return ([gnx.nodes(),test])

def graph_gml(Path):
		Path_Png = UPLOAD_FOLDER+"/upImg.png"
		graphNetworkx = nx.read_gml(Path)
		nx.draw(graphNetworkx)
		plt.savefig(Path_Png)
		return Path_Png

def callSendIPConf():
    status,output = cmds.getstatusoutput("python ./network/batch/sendpiconf.batch.py")
    print(status)
    print(output)

def callClearIPConf():
    status,output = cmds.getstatusoutput("python ./network/batch/clearpiconf.batch.py")
    print(status)
    print(output)

app.jinja_env.globals.update(callSendIPConf=callSendIPConf)
app.jinja_env.globals.update(get_this_edge=get_this_edge)
app.jinja_env.globals.update(remove_this_node=remove_this_node)

@app.route('/logout')
def logout():
	session.pop('username', None)
	status,output = cmds.getstatusoutput("python network/batch/clearpiconf.batch.py")
	status,output = cmds.getstatusoutput("echo '0' > network/infradpld")
	return redirect(url_for('login'))

@app.route('/block_chain', methods=['GET', 'POST'])
def block_chain():
	if request.method == 'POST':

		# Create the blockchain and add the genesis block
		blockchain = [create_genesis_block()]
		previous_block = blockchain[0]
		# How many blocks should we add to the chain
		# after the genesis block
		nb = request.form['nombre_block']
		num_of_blocks_to_add = int(nb)

		# Add blocks to the chain
		for i in range(0, num_of_blocks_to_add):
		  block_to_add = next_block(previous_block)
		  blockchain.append(block_to_add)
		  previous_block = block_to_add
		  # Tell everyone about it!
		  print "Block #{} has been added to the blockchain!".format(block_to_add.index)
		  flash("Block #{} has been added to the blockchain!".format(block_to_add.index))
		  flash("Hash: {}\n".format(block_to_add.hash))
		  print "Hash: {}\n".format(block_to_add.hash)
		return redirect(request.url)
	return render_template('BlockChain.html')

class Block:
  def __init__(self, index, timestamp, data, previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.hash_block()

  def hash_block(self):
    sha = hasher.sha256()
    sha.update(str(self.index) +
               str(self.timestamp) +
               str(self.data) +
               str(self.previous_hash))
    return sha.hexdigest()

def create_genesis_block():
  # Manually construct a block with
  # index zero and arbitrary previous hash
  return Block(0, date.datetime.now(), "Genesis Block", "0")

def laucheIP():
    status,output = cmds.getstatusoutput("python ./network/batch/getinfos.batch.py")

def getIP():
    file = open("./network/tmp/iplist.info", "r")
    return file.readlines()

def attributeIP(IP):
    gnx = nx.read_gml(UPLOAD_FOLDER+"up.gml")
    for idx, node in enumerate(gnx.nodes()):
        try:
            gnx.add_node(node,ip=IP[idx].replace("\n",""))
        except Exception as e:
            break
    nx.write_gml(gnx,UPLOAD_FOLDER+"up.gml")

def next_block(last_block):
  this_index = last_block.index + 1
  this_timestamp = date.datetime.now()
  this_data = "Hey! I'm block " + str(this_index)
  this_hash = last_block.hash
  return Block(this_index, this_timestamp, this_data, this_hash)
app.secret_key = "A0Zr98j/3yx R"

if __name__ == '__main__':
    laucheIP()
    app.run(debug=True)
