from pygltflib import GLTF2, Scene



gltf = GLTF2()
scene = Scene()

gltf.scenes.append(scene)

filename = "../../glTF-Sample-Models/v2/Avocado/glTF/Avocado.gltf"

gltf = GLTF2().load(filename)

#Meshes Data

for meshes in gltf.meshes:
    print(meshes.name)
    for primitives in meshes.primitives:
        print(primitives)

for buffers in gltf.buffers:
    print(buffers)
    print(buffers.uri)

#Meshes Textures
for images in gltf.images:
    print(images)
    print(images.uri)

for materials in gltf.materials:
    print('\033[95m' + materials.name)
