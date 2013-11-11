
class _Vertex:
    x = None
    y = None
    z = None

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class _Vertices:
    def __init__(self):
        pass

    vertices = {}

    def add(self, x, y, z, index=None):
        if index is None:
            index = len(self.vertices)

        self.vertices[index] = _Vertex(x, y, z)

class _Normal:
    x = None
    y = None
    z = None

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class _Normals:
    def __init__(self):
        pass

    normals = {}

    def add(self, x, y, z, index=None):
        if index is None:
            index = len(self.normals)

        self.normals[index] = _Normal(x, y, z)

class _Face:
    point1 = ()
    point2 = ()
    point3 = ()
    def __init__(self , point1, point2, point3):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3

class _Faces:
    def __init__(self):
        pass

    faces = []

    def add(self, point1, point2, point3):
        for list in (point1, point2, point3):
            for x in range(1,3):
                if list[x] != '':
                    list[x] = float(list[x])

        point1[0] = _Vertices.vertices[int(point1[0])-1]
        point1[1] = 0
        point1[2] = _Normals.normals[int(point1[2])-1]

        point2[0] = _Vertices.vertices[int(point2[0])-1]
        point2[1] = 0
        point2[2] = _Normals.normals[int(point2[2])-1]

        point3[0] = _Vertices.vertices[int(point3[0])-1]
        point3[1] = 0
        point3[2] = _Normals.normals[int(point3[2])-1]


        self.faces.append(_Face(point1, point2, point3))

    def getVertices(self):
        vertices = []
        for face in self.faces:
            for point in (face.point1, face.point2, face.point3):
                vertices.append([point[0].x, point[0].y, point[0].z])

        return  vertices

class Importer:
    def __init__(self):
        pass

    file = None

    vertices = _Vertices()
    normals = _Normals()
    faces = _Faces()


    def open(self, file):
        file = open(file, "r")

        for line in file:
            parts = line.split(" ")
            if parts[0] == "v":
                self.vertices.add(float(parts[1]), float(parts[2]), float(parts[3]))
            if parts[0] == "vn":
                self.normals.add(float(parts[1]), float(parts[2]), float(parts[3]))
            if parts[0] == "f":
                self.faces.add(parts[1].split("/"), parts[2].split("/"), parts[3].split("/"))

    def getArray(self):
        return self.faces.getVertices()