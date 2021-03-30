import vray

class Obj:
    def __init__(self):
        self.vertices = vray.VectorList()
        self.textureVertices = vray.VectorList()
        self.vertexNormals = vray.VectorList()
        self.faces = vray.IntList()
        self.faceTextures = vray.IntList()
        self.faceNormals = vray.IntList()
    def get_max_extent(self):
        vmin = [0, 0, 0]
        vmax = [0, 0, 0]
        for v in self.vertices:
            for i in range(3):
                if v[i] > vmax[i]:
                    vmax[i] = v[i]
                elif v[i] < vmin[i]:
                    vmin[i] = v[i]

        return max(vmax[0] - vmin[0], vmax[1] - vmin[1], vmax[2] - vmin[2])


class ConvexTriangulator:
    def triangulate(self, obj, vertexIndices):
        triangle = [None, None, None]
        triangle[0] = vertexIndices[0]
        triangle[1] = vertexIndices[1]
        for vertex in vertexIndices[2:]:
            triangle[2] = vertex

            for vertex in triangle:
                obj.faces.append(vertex[0])
                obj.faceTextures.append(vertex[1])
                obj.faceNormals.append(vertex[2])

            triangle[1] = triangle[2]


class ObjParser:
    def __init__(self, triangulator):
        self.triangulator = triangulator()

    def parse_file(self, file_name):
        obj = Obj()

        for line in open(file_name):
            self._parse_line(obj, line)

        return obj

    def _parse_line(self, obj, line):
        if line[0] == '#':
            return

        tokens = line.split()
        if len(tokens) == 0:
            return

        if tokens[0] == "v":
            self._parse_geometric_vertex(obj, tokens[1:])
        elif tokens[0] == "vt":
            self._parse_texture_vertex(obj, tokens[1:])
        elif tokens[0] == "vn":
            self._parse_vertex_normal(obj, tokens[1:])
        elif tokens[0] == "f":
            self._parse_face(obj, tokens[1:])

    def _parse_vertex_indices(self, arg):
        """Parses a v/vt/vn tuple.

        arg - String representation of the tuple.
        """

        indices = arg.split('/')

        v = int(indices[0]) - 1
        vt = -1
        vn = -1

        if len(indices) > 1 and len(indices[1]) > 0:
            vt = int(indices[1]) - 1

        if len(indices) > 2:
            vn = int(indices[2]) - 1

        return (v, vt, vn)

    def _parse_geometric_vertex(self, obj, args):
        """Parses a geometric vertex.

        obj - Structure representing the object.
        args - List of string representations of vertex components.
        """

        obj.vertices.append(vray.Vector(x=float(args[0]), y=float(args[1]), z=float(args[2])))

    def _parse_texture_vertex(self, obj, args):
        """Parses a texture vertex.

        obj - Structure representing the object.
        args - List of string representations of vertex components.
        """

        x = 0
        y = 0
        z = 0

        if len(args) >= 1:
            x = float(args[0])

        if len(args) >= 2:
            y = float(args[1])

        if len(args) >= 3:
            z = float(args[2])

        obj.textureVertices.append(vray.Vector(x, y, z))

    def _parse_vertex_normal(self, obj, args):
        """Parses a normal vertex.

        obj - Structure representing the object.
        args - List of string representations of vertex components.
        """

        obj.vertexNormals.append(vray.Vector(x=float(args[0]), y=float(args[1]), z=float(args[2])))

    def _parse_face(self, obj, args):
        """Parses and triangulates a face.

        obj - Structure representing the object.
        args - List of string representations of tuples of the form v/vt/vn.
        """

        vertexIndices = [self._parse_vertex_indices(arg) for arg in args]
        self.triangulator.triangulate(obj, vertexIndices)
