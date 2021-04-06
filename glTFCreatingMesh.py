from struct import *
import numpy as np
from pygltflib import *


def gltfCreatingMesh(width, length):
    vertices = np.array(
        [
            [-width/2, 0, -length/2],
            [width/2, 0, -length/2],
            [-width/2, 0, length/2],
            [width/2, 0, length/2],
        ],
        dtype="float32",
    )
    triangles = np.array(
        [
            [0, 1, 2],
            [3, 2, 1],
        ],
        dtype="uint8",
    )

    triangles_binary_blob = triangles.flatten().tobytes()
    points_binary_blob = vertices.tobytes()

    gltf = GLTF2(
        asset=[
            Asset(
            )
        ],
        scene=0,
        scenes=[
            Scene(
                name="Scene",
                nodes=[0]
            )
        ],
        nodes=[
            Node(
                mesh=0,
                name="Plane"
            )
        ],
        meshes=[
            Mesh(
                primitives=[
                    Primitive(
                        attributes=Attributes(
                            POSITION=1,
                            #NORMAL=1,
                            #TEXCOORD_0=2
                            ),
                        indices=0,
                        material=0
                    )
                ]
            )
        ],
        accessors=[
            Accessor(
                bufferView=0,
                componentType=UNSIGNED_BYTE,
                count=triangles.size,
                type=SCALAR,
                max=[int(triangles.max())],
                min=[int(triangles.min())],
            ),
            Accessor(
                bufferView=1,
                componentType=FLOAT,
                count=len(vertices),
                type=VEC3,
                max=vertices.max(axis=0).tolist(),
                min=vertices.min(axis=0).tolist(),
            ),
        ],
        bufferViews=[
            BufferView(
                buffer=0,
                byteLength=len(triangles_binary_blob),
                target=ELEMENT_ARRAY_BUFFER,
            ),
            BufferView(
                buffer=0,
                byteOffset=len(triangles_binary_blob),
                byteLength=len(points_binary_blob),
                target=ARRAY_BUFFER,
            ),
        ],
        materials=[
            Material(
                alphaMode=OPAQUE,
                alphaCutoff=0.0,
                doubleSided=True,
                name="Material.001",
                pbrMetallicRoughness=PbrMetallicRoughness(
                    #baseColorTexture=0,
                    baseColorFactor=[0.0, 0.0, 0.0, 0.0],
                ),
            )
        ],
        textures=[
            Texture(
            )
        ],
        buffers=[
            Buffer(
                byteLength=len(triangles_binary_blob) + len(points_binary_blob)
            )
        ],
    )
    gltf.set_binary_blob(triangles_binary_blob + points_binary_blob)
    gltf.save("plane.glb")

if __name__ == "__main__":
   gltfCreatingMesh(5, 5)