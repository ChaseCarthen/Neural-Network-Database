import numpy as np 
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from torchutils import torchextract
from database import insert,tables
from torchvision import models as tmodels
import json
from pathlib import Path
from onnxutils.onnxextract import extract_compute_graph_taxonomy_style

def write_to_database(data):
    engine = db.create_engine('postgresql://username:password@localhost/graphdb')
    Session = sessionmaker(bind=engine)
    session = Session()

    dbmodel = tables.Model()
    dbmodel.model_name = data['name']
    dbmodel.library = data['library']
    dbmodel.graph = data['graph']

    layers = []
    parameters = []
    interparameters = []
    summ = np.zeros((256))
    count = 0
    for item in data['network']:
        layer = tables.Layer()
        layer.layer_name = item['name']
        layer.attributes = json.dumps(item['attributes'])
        layer.known_type = item['type']
        layer.model=dbmodel
        for parameter in item['parameters']:
            param = tables.Parameter()
            param.parameter_name = parameter['name']
            param.shape = str(parameter['shape'])
            param.layer = layer
            interpolated = np.nan_to_num(np.array(parameter['interpolated_vector']), nan=0.0)
            param.weight_embedding = interpolated
            summ = summ * (count / (count+1)) + (interpolated) / (count+1)
            count += 1
            parameters.append(param)
        layers.append(layer)
    dbmodel.average_weight_embedding = summ 
    session.add(dbmodel)
    session.commit() 

if __name__ == '__main__':
    engine = db.create_engine('postgresql://username:password@localhost/graphdb')
    Session = sessionmaker(bind=engine)
    session = Session()

    for path in Path('/fastdata2/data/onnxfiles/models/validated/').rglob('*.onnx'):
        write_to_database(extract_compute_graph_taxonomy_style(path,savePath='',parameters=False,writeFile=False))
        


    models  = [ 'alexnet','googlenet','regnet_y_400mf','swin_t','squeezenet1_0','inception_v3', 'resnet101', 'resnet152', 'resnet18', 'resnet34', 'resnet50', 'vgg11', 'vgg11_bn', 'vgg13', 'vgg13_bn', 'vgg16', 'vgg16_bn', 'vgg19', 'vgg19_bn','vit_b_16','vit_b_32','vit_l_16','vit_l_32','vit_h_14']   
    for modelname in models:
        model = tmodels.get_model(modelname,weights="DEFAULT")
        data = torchextract.extract_model_properties(model, name=modelname)
        write_to_database(data)
