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
    vrayVectorList = vray.VectorList()
    for v in vertc:
        vrayVector = vray.Vector(v[0], v[1], v[2])
        vrayVectorList.append(vrayVector)
    return vrayVectorList

def to_int_list(vrayIList):
    vrayIntList = vray.IntList()
    for i in vrayIList:
        vrayIntList.append(i)
    #print(vrayIntList)
    return vrayIntList



def add_obj(renderer, material, smooth=False):

    if len(vertices) == 0 or len(faces) == 0:
        return
    mesh = renderer.classes.GeomStaticMesh()
    mesh.vertices = to_vector_list(vertices)
    mesh.faces = to_int_list(faces)

    #if len(obj.vertexNormals) > 0 and len(obj.faceNormals) > 0:
    #   mesh.normals = obj.vertexNormals
    #   mmesh.faceNormals = obj.faceNormals

    #if len(obj.textureVertices) > 0 and len(obj.faceTextures) > 0:
    #   channel = [1, obj.textureVertices, obj.faceTextures]
    #   mesh.map_channels = [channel]

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
    gltf_loader(filename="../../glTF-Sample-Models/sugartech/tp_livelokonsol_High1433.glb")
    to_int_list(faces)
    with vray.VRayRenderer() as renderer:
        renderer.keepInteractiveRunning = True

        brdf = renderer.classes.BRDFVRayMtl()
        brdf.diffuse = vray.AColor(0.5, 1.0, 0.5, 1.0)
        brdf.reflect = vray.AColor(0.8, 0.8, 0.8, 1.0)
        brdf.fresnel = True
        material = renderer.classes.MtlSingleBRDF()
        material.brdf = brdf

        parser = ObjParser(triangulator=ConvexTriangulator)
        add_obj(renderer, material)

        setup_scene(renderer, 3)

        # you can use the VFB mouse controls to orbit around the object
        # (shift + LMB drag)
        renderer.start()
        renderer.waitForRenderEnd()