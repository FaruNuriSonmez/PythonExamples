from struct import *
import numpy as np
from pygltflib import *

vertices = []
faces = []
def gltf_loader(filename):
    gltf = GLTF2.load(filename)
    mesh = gltf.meshes[gltf.scenes[gltf.scene].nodes[0]]
    for primitive in mesh.primitives:
        accessorPosition = gltf.accessors[primitive.attributes.POSITION]
        bufferView = gltf.bufferViews[accessorPosition.bufferView]
        buffer = gltf.buffers[bufferView.buffer]
        binary_blob = gltf.binary_blob()

        for i in range(accessorPosition.count):
            index = bufferView.byteOffset + accessorPosition.byteOffset + i * 12  # the location in the buffer of this vertex
            d = binary_blob[index:index + 12]  # the vertex data
            v = struct.unpack("<fff", d)  # convert from base64 to three floats
            vertices.append(v)

        accessorIndice = gltf.accessors[primitive.indices]
        bufferViewIndices = gltf.bufferViews[accessorIndice.bufferView]
        buffer = gltf.buffers[bufferView.buffer]
        indices = np.frombuffer(
            binary_blob[
            bufferViewIndices.byteOffset
            + accessorIndice.byteOffset: bufferViewIndices.byteOffset
                                         + bufferViewIndices.byteLength
            ],
            dtype="uint16",
            count=accessorIndice.count, )
        for i in indices:
            faces.append(i)