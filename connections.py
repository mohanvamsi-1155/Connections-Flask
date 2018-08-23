from __future__ import division, print_function
import os
import io
import sys
import re
import numpy as np
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from matplotlib import pyplot as plt
import networkx as nx
import pandas as pd
app = Flask(__name__)
print("UI started. Connect at http://127.0.0.1:5000")
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        f = request.files['file']
        print(request.name)
        data = pd.read_csv(f)
        img = io.BytesIO()
        print(data.info())
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
        print(request)
        name="Srikar"
        data.Name.fillna(data.Number, inplace=True)
        index_list = data['Name'].value_counts().index.tolist()
        counts = data['Name'].value_counts().tolist()
        data_for_nx = dict()
        colors = []
        for i in range(len(index_list)):
            data_for_nx[index_list[i]] = counts[i]
        print(colors)
        print(counts)
        g = nx.Graph()
        g.add_node(name)
        nodes = []
        for i in range(len(index_list)):
            nodes.append((name,index_list[i]))
        g.add_edges_from(nodes)
        nx.draw(g, nodelist=data_for_nx.keys(), node_size=[v * 100 for v in data_for_nx.values()],with_labels=True)
        filename = "Graph.png"
        plt.savefig(filename, format="PNG")
        return filename
    return None
if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
