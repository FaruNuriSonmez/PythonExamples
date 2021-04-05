from pygltflib import GLTF2, Scene
from pygltflib.utils import ImageFormat, Image

gltf = GLTF2()
scene = Scene()
filename = "../glTF-Sample-Models/sugartech/tp_livelokonsol_High1433.glb"
texturePath = "./assets/textures"

gltf = GLTF2.load(filename)
print(type(len(gltf.images)))

i = -1
while i < len(gltf.images)-1:
    i += 1
    gltf.images[i].name = "texture"
    gltf.images[i].mimeType = 'image/png'
gltf.convert_images(ImageFormat.FILE, path=texturePath)

print()