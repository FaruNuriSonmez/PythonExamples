import struct
import numpy as np
from pygltflib import GLTF2

filename = "../glTF-Sample-Models/sugartech/tp_livelokonsol_High1433.glb"
gltf = GLTF2().load(filename)

mesh = gltf.meshes[gltf.scenes[gltf.scene].nodes[0]]
for primitive in mesh.primitives:
    accessorPosition = gltf.accessors[primitive.attributes.POSITION]
    bufferView = gltf.bufferViews[accessorPosition.bufferView]
    buffer = gltf.buffers[bufferView.buffer]
    binary_blob = gltf.binary_blob()

    #print(primitive.attributes.POSITION)
    #print(gltf.accessors[primitive.attributes.POSITION])

    #print(primitive.attributes.NORMAL)
    #print(gltf.accessors[primitive.attributes.NORMAL])

    #print(primitive.indices)
    #print(gltf.accessors[primitive.indices])

    #print(primitive.attributes.TEXCOORD_0)
    #print(gltf.accessors[primitive.attributes.TEXCOORD_0])

    #print(gltf.accessors[primitive.attributes.TANGENT])

    primitive_mat = gltf.materials[primitive.material]
    print(primitive_mat.normalTexture)

    #print(gltf.images[gltf.materials[primitive.material].pbrMetallicRoughness.metallicRoughnessTexture.index])
    #print(gltf.bufferViews[5])

    vertices = []
    textureVertices = []
    textureFaces = []
    for i in range(accessorPosition.count):
        index = bufferView.byteOffset + accessorPosition.byteOffset + i * 12  # the location in the buffer of this vertex
        d = binary_blob[index:index + 12]  # the vertex data
        v = struct.unpack("<fff", d)  # convert from base64 to three floats

        vertices.append(v[0])
        vertices.append(v[1])
        vertices.append(v[2])
        #print(i, v)
    #print(len(vertices))
    #print(gltf.accessors)
    accessorIndice = gltf.accessors[primitive.indices]
    bufferViewIndices = gltf.bufferViews[accessorIndice.bufferView]
    buffer = gltf.buffers[bufferView.buffer]
    #print(vertices)
    indices = np.frombuffer(
        binary_blob[
        bufferViewIndices.byteOffset
        + accessorIndice.byteOffset: bufferViewIndices.byteOffset
                                         + bufferViewIndices.byteLength
        ],
        dtype="uint16",
        count=accessorIndice.count)

    #print(len(indices))
    #for i in indices:
        #print(i)

    if primitive.attributes:
        if primitive.attributes.TEXCOORD_0 != None:
            accessorTextures = gltf.accessors[primitive.attributes.TEXCOORD_0]
        if primitive.attributes.TEXCOORD_1 != None:
            accessorTextures = gltf.accessors[primitive.attributes.TEXCOORD_1]

    bufferViewTextures = gltf.bufferViews[accessorTextures.bufferView]
    #print(gltf.bufferViews)

    for i in range(accessorTextures.count):
        index = bufferViewTextures.byteOffset + accessorTextures.byteOffset + i * 8  # the location in the buffer of this vertex
        d = binary_blob[index:index + 8]  # the vertex data
        v = struct.unpack("<ff", d)  # convert from base64 to three floats
        textureVertices.append(v)
        #print(i, v)




