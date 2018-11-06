# coding: utf8
import os
from flask import Flask, flash, session, redirect, url_for, escape, request, render_template, jsonify, json
from werkzeug.utils import secure_filename
import networkx as nx
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph

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

        print (request.form)
        print ('newNode' in request.form)
        print ('deleteNode' in request.form)
        print ('linknode' in request.form)

        if 'file' not in request.files:
            if 'newNode' in request.form:
                nodes = add_this_node(request.form["nodename"])
                edges = get_edges(UPLOAD_FOLDER+"up.gml")
                return render_template('appgml.html',error=error,nodes=nodes,edges=edges)
            elif 'deleteNode' in request.form:
                nodes = remove_this_node(request.form["nodeD"])
                edges = get_edges(UPLOAD_FOLDER+"up.gml")
                return render_template('appgml.html',error=error,nodes=nodes,edges=edges)

            elif 'linknode' in request.form:
                nodes,result = add_egde(request.form["node1"],request.form["node2"])
                edges = get_edges(UPLOAD_FOLDER+"up.gml")
                return render_template('appgml.html',error=error,nodes=nodes,edges=edges,result=result)
            else:
                return redirect(url_for('appgml',error='no in request file'))

        file = request.files['file']
        if file.filename == '':
            return redirect(url_for('appgml',error='no selected file'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            test = get_nodes(UPLOAD_FOLDER+"up.gml")
            test2 = get_edges(UPLOAD_FOLDER+"up.gml")
            return render_template('appgml.html',error=error,nodes=test,edges=test2)

    else:
        return render_template('appgml.html',error=error)


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
    print(result)
    return(result)

def remove_this_node(node):
    gnx = nx.read_gml(UPLOAD_FOLDER+"up.gml")
    gnx.remove_node(node)
    nx.write_gml(gnx,UPLOAD_FOLDER+"up.gml")
    return (gnx.nodes())

def add_this_node(node):
    gnx = nx.read_gml(UPLOAD_FOLDER+"up.gml")
    gnx.add_node(node)
    nx.write_gml(gnx,UPLOAD_FOLDER+"up.gml")
    return (gnx.nodes())

def add_egde(nodeSource,nodeDest):
    gnx = nx.read_gml(UPLOAD_FOLDER+"up.gml")
    test = gnx.add_edge(nodeSource,nodeDest)
    nx.write_gml(gnx,UPLOAD_FOLDER+"up.gml")
    return ([gnx.nodes(),test])

app.jinja_env.globals.update(get_this_edge=get_this_edge)
app.jinja_env.globals.update(remove_this_node=remove_this_node)

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/graph')
def graph():
    gnx = nx.read_gml(UPLOAD_FOLDER+"up.gml")
    data = json_graph.node_link_data(gnx)
    with open('graph.json', 'w') as f:
        json.dump(data, f, indent=4)
    print(data)
    #print(f)
    return("hello")

app.secret_key = "A0Zr98j/3yx R"
if __name__ == '__main__':
    app.run(debug=True)
