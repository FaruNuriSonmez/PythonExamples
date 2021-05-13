from struct import *
import numpy as np
from pygltflib import *

def gltfCreatingMesh(width, length, texture):
    vertices = np.array(
        [
            [-width/2, 0, -length/2],
            [width/2, 0, -length/2],
            [-width/2, 0, length/2],
            [width/2, 0, length/2],
        ],
        dtype="float32",
    )

    normals = np.array(
        [
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0],
        ],
        dtype="float32",
    )

    indices = np.array(
        [
            [2, 1, 0],
            [1, 2, 3],
        ],
        dtype="uint8",
    )

    texture_coordinates = np.array(
        [
            [0.0, 0.0],
            [1.0, 0.0],
            [0.0, 1.0],
            [1.0, 1.0],
        ],
        dtype="float32"
    )

    indices_binary_blob = indices.flatten().tobytes()
    vertices_binary_blob = vertices.tobytes()
    texture_coordinates_binary_blob = texture_coordinates.tobytes()
    normals_binary_blob = normals.tobytes()

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
                            NORMAL=3,
                            TEXCOORD_0=2
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
                count=indices.size,
                type=SCALAR,
                max=[int(indices.max())],
                min=[int(indices.min())],
            ),
            Accessor(
                bufferView=1,
                componentType=FLOAT,
                count=len(vertices),
                type=VEC3,
                max=vertices.max(axis=0).tolist(),
                min=vertices.min(axis=0).tolist(),
            ),
            Accessor(
                bufferView=2,
                componentType=FLOAT,
                count=len(texture_coordinates),
                type=VEC2,
                max=texture_coordinates.max(axis=0).tolist(),
                min=texture_coordinates.min(axis=0).tolist(),
            ),
            Accessor(
                bufferView=3,
                componentType=FLOAT,
                count=len(normals),
                type=VEC3

            ),
        ],
        bufferViews=[
            BufferView(
                buffer=0,
                byteLength=len(indices_binary_blob),
                target=ELEMENT_ARRAY_BUFFER,
            ),
            BufferView(
                buffer=0,
                byteOffset=len(indices_binary_blob),
                byteLength=len(vertices_binary_blob),
                target=ARRAY_BUFFER,
            ),

            BufferView(
                buffer=0,
                byteOffset=len(indices_binary_blob) +
                len(vertices_binary_blob),
                byteLength=len(texture_coordinates_binary_blob),
                target=ARRAY_BUFFER,
            ),

            BufferView(
                buffer=0,
                byteOffset=len(indices_binary_blob) +
                len(vertices_binary_blob) +
                len(texture_coordinates_binary_blob),
                byteLength=len(normals_binary_blob),
                target=ARRAY_BUFFER,
            ),
        ],
        materials=[
            Material(
                alphaMode=BLEND,
                #alphaMode=OPAQUE,
                doubleSided=True,
                name="Material.001",
                pbrMetallicRoughness=PbrMetallicRoughness(
                    baseColorTexture=TextureInfo(
                        index=0,),
                ),
            )
        ],
        textures=[
            Texture(
                source=0,
                name='name'
            )
        ],

        buffers=[
            Buffer(
                byteLength=len(indices_binary_blob) + len(vertices_binary_blob) +
                len(texture_coordinates_binary_blob) + len(normals_binary_blob)
            )
        ],
    )
    image = Image()
    image.uri = texture
    image.name = "resimName"
    gltf.images.append(image)
    gltf.convert_images(ImageFormat.DATAURI)
    gltf.set_binary_blob(indices_binary_blob + vertices_binary_blob +
                         texture_coordinates_binary_blob + normals_binary_blob)
    gltf.save("plane.glb")


if __name__ == "__main__":
    gltfCreatingMesh(10, 5, "/alphaChannel.png")
