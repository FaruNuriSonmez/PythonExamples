from __future__ import print_function

from objParser import *
import os, math
from glTFVRayLoader import *
SCENE_PATH = os.path.join(os.environ.get('VRAY_SDK'), 'scenes')


def make_transform(rotX=0, rotY=0, rotZ=0, scale=1, offset=vray.Vector()):
    """Creates a transform with the specified rotation and scale.
    """
    mS = vray.Matrix(scale)
    mX = vray.Matrix.makeRotationMatrixX(rotX)
    mY = vray.Matrix.makeRotationMatrixY(rotY)
    mZ = vray.Matrix.makeRotationMatrixZ(rotZ)
    transform = vray.Transform(mS * mZ * mY * mX, offset)
    return transform

def setup_scene(renderer, obj_diameter):
    renderView = renderer.classes.RenderView()

    camPos = vray.Vector(0, -2 * obj_diameter, 0.2 * obj_diameter)
    camTransform = make_transform(math.pi / 2, 0, 0, 1, camPos)
    renderView.transform = camTransform

    dome = renderer.classes.LightDome()
    dome.transform = make_transform()
    dome.intensity = 0.25

    # place a light over and slightly behind the camera
    rect = renderer.classes.LightRectangle()
    adjust = make_transform(-math.pi / 9, 0, math.pi / 3, 1, 0.1 * camPos)
    rect.transform = adjust * camTransform
    rect.u_size = 0.5 * obj_diameter
    rect.v_size = 0.35 * obj_diameter
    rect.intensity = 10


def to_vector_list(vertc):
    #print(vertc)
    vrayVectorList = vray.VectorList()
    i = 0
    while i < len(vertc):
        vrayVector = vray.Vector(vertc[i], vertc[i+1], vertc[i+2])
        i += 3
        vrayVectorList.append(vrayVector)
    #print(vrayVectorList)
    return vrayVectorList

def to_int_list(vrayIList):
    vrayIntList = vray.IntList()
    for i in vrayIList:
        vrayIntList.append(i)
    #print(vrayIntList)
    return vrayIntList

def to_textures_vector_list(vectors):
    #print(vectors)
    vrayVectorList = vray.VectorList()
    i = 0
    while i < len(vectors):
        vrayVector = vray.Vector(vectors[i], vectors[i + 1], 0)
        i += 2
        vrayVectorList.append(vrayVector)

    return vrayVectorList

def add_obj(renderer, material, smooth=False):
    if len(vertices) == 0 or len(faces) == 0:
        return
    mesh = renderer.classes.GeomStaticMesh()
    mesh.vertices = to_vector_list(vertices)
    mesh.faces = to_int_list(faces)

    #if len(obj.vertexNormals) > 0 and len(obj.faceNormals) > 0:
    #   mesh.normals = obj.vertexNormals
    #   mmesh.faceNormals = obj.faceNormals

    if len(texturesVertices) > 0 and len(texturesFaces) > 0:
        vrayTexturesVertices = to_textures_vector_list(texturesVertices)
        channel = [1, vrayTexturesVertices, mesh.faces]
        mesh.map_channels = [channel]

    if smooth:
        smoothed = renderer.classes.GeomStaticSmoothedMesh()
        smoothed.mesh = mesh
        mesh = smoothed

    node = renderer.classes.Node()
    node.geometry = mesh
    node.material = material
    # adjust Y-up object to Z-up scene
    node.transform = make_transform(math.pi / 2, 0, 0)

if __name__ == "__main__":
    GLTFVRayLoader.gltf_loader(filepath="../../glTF-Sample-Models/sugartech/tp_livelokonsol_High1433.glb", texpath=".././assets/textures")
    with vray.VRayRenderer() as renderer:

        renderer.keepInteractiveRunning = True

        bitmap = renderer.classes.BitmapBuffer()
        bitmap.file = "/Users/farunurisonmez/Documents/GitHub/PythonExamples/assets/textures/3.png"

        normalBitmap = renderer.classes.BitmapBuffer()
        normalBitmap.file = "/Users/farunurisonmez/Documents/GitHub/PythonExamples/assets/textures/1.png"

        texture = renderer.classes.TexBitmap()
        texture.bitmap = bitmap

        normalTexture = renderer.classes.TexBitmap()
        normalTexture.bitmap = normalBitmap

        brdf = renderer.classes.BRDFVRayMtl()
        brdf.diffuse = texture
        brdf.bump_map = normalTexture
        brdf.reflect = vray.AColor(0.8, 0.8, 0.8, 1.0)
        brdf.fresnel = True

        x = renderer.classes.BRDFAlSurface()
        x.diffuse = texture
        x.bump_map = normalTexture
        x.bump_type = 6


        material = renderer.classes.MtlSingleBRDF()
        material.brdf = texture

        parser = ObjParser(triangulator=ConvexTriangulator)
        add_obj(renderer, material)

        setup_scene(renderer, 3)
        # you can use the VFB mouse controls to orbit around the object
        # (shift + LMB drag)

        renderer.start()
        renderer.waitForRenderEnd()