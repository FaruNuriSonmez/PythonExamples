from pygltflib import GLTF2, Scene
from pygltflib.utils import ImageFormat

gltf = GLTF2()
scene = Scene()

filename = "../glTF-Sample-Models/2.0/AnimatedCube/glTF/AnimatedCube.gltf"

gltf = GLTF2.load(filename)
gltf.images[0].name = "cube.png"
gltf.convert_images(ImageFormat.FILE, path='/textures/')

gltf.images[0].uri


