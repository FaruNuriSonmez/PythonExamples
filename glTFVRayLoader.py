from struct import *
import numpy as np
import DracoPy as dp
from pygltflib import *

vertices = []
faces = []
texturesVertices = []
texturesFaces = []

class GLTFVRayLoader:
    def gltf_loader(filepath,texpath):
        gltf = GLTF2.load(filepath)
        if len(gltf.extensionsUsed) > 1:
            if (gltf.extensionsUsed[1] == 'KHR_draco_mesh_compression'):
                mesh = gltf.meshes[0]
                for primitive in mesh.primitives:
                    a = primitive.extensions['KHR_draco_mesh_compression']
                    bufferView = gltf.bufferViews[a["bufferView"]]
                    binary_blob = gltf.binary_blob()
                    binary_data = binary_blob[bufferView.byteOffset: bufferView.byteOffset + bufferView.byteLength]
                    undraco = dp.decode_buffer_to_mesh(binary_data)
                for v in undraco.data_struct["points"]:
                    vertices.append(float(v))
                for i in undraco.data_struct["faces"]:
                    faces.append(i)
        else:
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
                    vertices.append(v[0])
                    vertices.append(v[1])
                    vertices.append(v[2])

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

                if primitive.attributes.TEXCOORD_0 != None:
                    accessorTextures = gltf.accessors[primitive.attributes.TEXCOORD_0]
                if primitive.attributes.TEXCOORD_1 != None:
                    accessorTextures = gltf.accessors[primitive.attributes.TEXCOORD_1]

                bufferViewTextures = gltf.bufferViews[accessorTextures.bufferView]

                for i in range(accessorTextures.count):
                    index = bufferViewTextures.byteOffset + accessorTextures.byteOffset + i * 8  # the location in the buffer of this vertex
                    d = binary_blob[index:index + 8]  # the vertex data
                    v = struct.unpack("<ff", d)  # convert from base64 to three floats
                    texturesVertices.append(v[0])
                    texturesVertices.append(v[1])
                    texturesFaces.append(i)

                i = -1
                while i < len(gltf.images)-1:
                    i += 1
                    gltf.images[i].mimeType = 'image/png'
                gltf.convert_images(ImageFormat.FILE, path=texpath)
