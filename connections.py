from __future__ import division, print_function
import os,sys,re,time,datetime
import numpy as np
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from matplotlib import pyplot as plt
from pylab import rcParams
import networkx as nx
import pandas as pd
plt.rcParams["figure.figsize"] = (15,10)
app = Flask(__name__)
print("UI started. Connect at http://127.0.0.1:5000")
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        f = request.files['file']
        name = request.form['username']
        data = pd.read_csv(f)
        '''
        <class 'pandas.core.frame.DataFrame'>
        RangeIndex: 484 entries, 0 to 483
        Data columns (total 8 columns):
        SI No                484 non-null int64
        Name                 369 non-null object
        Type                 331 non-null object
        Number               484 non-null int64
        Call Type            484 non-null object
        Time                 484 non-null object
        Duration             484 non-null object
        Duration(Seconds)    484 non-null int64
        dtypes: int64(3), object(5)
        memory usage: 30.3+ KB
        '''
        data.Name.fillna(data.Number, inplace=True)
        index_list = data['Name'].value_counts().index.tolist()
        counts = data['Name'].value_counts().tolist()
        data_for_nx = dict()
        for i in range(len(index_list)):
            data_for_nx[index_list[i]] = counts[i]
        g = nx.Graph()
        g.add_node(name)
        nodes = []
        for i in range(len(index_list)):
            nodes.append((name,index_list[i]))
        g.add_edges_from(nodes)
        nx.draw(g, nodelist=data_for_nx.keys(), node_size=[v * 100 for v in data_for_nx.values()],with_labels=True)
        ts = time.time()    
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        basepath = os.path.dirname(__file__)
        img = "uploads/{}_{}.png".format(st,name)
        plt.savefig(img, dpi=300, format="PNG")
        plt.clf()
        return img
    return None
if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()

