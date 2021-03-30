import pathlib
import struct

import numpy as np
from pprint import pprint

import DracoPy as dp

from pygltflib import GLTF2

filename = "../glTF-Sample-Models/sugartech/tp_livelokonsol_High1433d.glb"
gltf = GLTF2().load(filename)
print(gltf.extensionsUsed)

if len(gltf.extensionsUsed) > 1:
    if gltf.extensionsUsed[1] == 'KHR_draco_mesh_compression':
        print("True")
    else:
        print('dracooo değil')

print(type(gltf.extensionsUsed))
print(len(gltf.meshes))
mesh = gltf.meshes[0]#.extensions['KHR_draco_mesh_compression']

vertices = []
for primitive in mesh.primitives:
    a = primitive.extensions['KHR_draco_mesh_compression']
    bufferView = gltf.bufferViews[a["bufferView"]]
    attributes = a["attributes"]["POSITION"]
    accesor = gltf.accessors[attributes]
    buffer = gltf.buffers[bufferView.buffer]
    #print(bufferView)
    binary_blob = gltf.binary_blob()
    binary_data = binary_blob[bufferView.byteOffset: bufferView.byteOffset + bufferView.byteLength]
    undraco = dp.decode_buffer_to_mesh(binary_data)

    #v = struct.unpack("<fff", undraco.data_struct["points"])
    #vertices.append(v)
    #print(len(undraco.data_struct["faces"]))
    print(undraco.data_struct["points"])