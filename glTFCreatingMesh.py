import numpy as np
from pygltflib import *
import sys as sys
from PIL import Image as pil
import io



def ThumbFromBuffer(texture):
    im =  Image.open(texture)
    im.thumbnail((1024,1024),Image.ANTIALIAS)
    return im.tobytes()

def readImagesAsBinary(texture):
    
    im = pil.open(texture)
    im.thumbnail((1024,1024),pil.ANTIALIAS)
    ioSave = io.BytesIO()
    im.save(ioSave,format=("PNG"))
    image_binary_blob= ioSave.getvalue()
    bit = 4 - (len(image_binary_blob) % 4)

    for i in range(bit):
        image_binary_blob += bytes([0x000])
    return image_binary_blob 


def gltfCreatingMesh(width, length, texture, output):

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
    image_binary_blob= readImagesAsBinary(texture)

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

             BufferView(
                buffer=0,
                byteOffset=len(indices_binary_blob) +
                len(vertices_binary_blob) +
                len(texture_coordinates_binary_blob) + len(normals_binary_blob),
                byteLength=len(image_binary_blob) ,
                
            ),
        ],
        materials=[
            Material(
                alphaMode=MASK,
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
                name='name',
            )
        ],
        images = [
            Image( 
                mimeType= "image/png",
                bufferView= 4
              )
        ],

        buffers=[
            Buffer(
                byteLength=len(indices_binary_blob) + len(vertices_binary_blob) +
                len(texture_coordinates_binary_blob) + len(normals_binary_blob) + len(image_binary_blob)
            )
        ],
    )
    image = Image()
    image.uri = texture
    image.name = "resimName"
    #gltf.images.append(image)
   # gltf.convert_images(ImageFormat.DATAURI)
    gltf.set_binary_blob(indices_binary_blob + vertices_binary_blob +
                         texture_coordinates_binary_blob + normals_binary_blob + image_binary_blob )

    #gltf.convert_buffers(BufferFormat.BINARYBLOB)

    gltf.save(output + "plane.glb")

    print(len(image_binary_blob) )

if __name__ == "__main__":
     gltfCreatingMesh(float(sys.argv[1]), float(sys.argv[2]), sys.argv[3], sys.argv[4])
