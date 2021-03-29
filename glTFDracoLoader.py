import pathlib
import struct

import miniball as nb
import numpy as np
from pprint import pprint

import DracoPy as dp

from pygltflib import GLTF2

filename = "../glTF-Sample-Models/sugartech/109142Com_d.glb"

gltf = GLTF2().load(filename)

# mesh = gltf.meshes[gltf.scenes[gltf.scene].nodes[0]]

mesh = gltf.meshes[3]#.extensions['KHR_draco_mesh_compression']

for primitive in mesh.primitives:
    a = primitive.extensions['KHR_draco_mesh_compression']
    bufferView = gltf.bufferViews[a["bufferView"]]
    attributes = a["attributes"]["POSITION"]
    accesor = gltf.accessors[attributes]
    buffer = gltf.buffers[bufferView.buffer]

    binary_blob = gltf.binary_blob()
    binary_data = binary_blob[bufferView.byteOffset: bufferView.byteOffset + bufferView.byteLength]
    undraco = dp.decode_buffer_to_mesh(binary_data)
    print(undraco.data_struct["points"])
    print(undraco.data_struct["faces"])
    #print(accesor)

#for primitive in mesh.primitives:
#    accessorPosition = gltf.accessors[primitive.attributes.POSITION]