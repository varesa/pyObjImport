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


class _TextureCoord:

    x = None
    y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y


class _TextureCoords:
    def __init__(self):
        pass

    texturecoords = {}

    def add(self, x, y, index=None):
        if index is None:
            index = len(self.texturecoords)
        self.texturecoords[index] = _TextureCoord(x, y)


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
        point1[1] = _TextureCoords.texturecoords[int(point1[1])-1]
        point1[2] = _Normals.normals[int(point1[2])-1]

        point2[0] = _Vertices.vertices[int(point2[0])-1]
        point2[1] = _TextureCoords.texturecoords[int(point2[1])-1]
        point2[2] = _Normals.normals[int(point2[2])-1]

        point3[0] = _Vertices.vertices[int(point3[0])-1]
        point3[1] = _TextureCoords.texturecoords[int(point3[1])-1]
        point3[2] = _Normals.normals[int(point3[2])-1]


        self.faces.append(_Face(point1, point2, point3))

    def getVertices(self):
        vertices = []
        for face in self.faces:
            for point in (face.point1, face.point2, face.point3):
                print(point)
                vertices.append([point[0].x, point[0].y, point[0].z, point[1].x, point[1].y, point[2].x, point[2].y, point[2].z])

        return  vertices


class _MaterialLib:

    materials = None

    def __init__(self, materials):
        self.materials = materials

    def load(self, file):
        lib = open(file, "r")

        lastnew = None

        for line in lib:
            parts = line.split()
            if len(parts) == 0:
                continue
            if parts[0] == "newmtl":
                lastnew = self.materials.add(parts[1])
            if parts[0] == "Ns":
                self.materials.materials[lastnew].Ns = float(parts[1])
            if parts[0] == "Ka":
                self.materials.materials[lastnew].Ka = float(parts[1])
            if parts[0] == "Kd":
                self.materials.materials[lastnew].Kd = float(parts[1])
            if parts[0] == "Ks":
                self.materials.materials[lastnew].Ks = float(parts[1])
            if parts[0] == "Ki":
                self.materials.materials[lastnew].Ki = float(parts[1])
            if parts[0] == "d":
                self.materials.materials[lastnew].d = float(parts[1])
            if parts[0] == "illum":
                self.materials.materials[lastnew].illum = float(parts[1])
            if parts[0] == "map_Kd":
                self.materials.materials[lastnew].map_Kd = " ".join(parts[1:])

        lib.close()


class _Material:
    name = None
    Ns = None
    Ka = None
    Kd = None
    Ks = None
    Ni = None
    d = None
    illum = None
    map_Kd = None

    def __init__(self):
        pass


class _Materials:
    def __init__(self):
        pass

    materials = {}

    def add(self, name):
        self.materials[name] = _Material()
        self.materials[name].name = name
        return name


class Importer:
    def __init__(self):
        pass

    file = None

    vertices = _Vertices()
    texturecoords = _TextureCoords()
    normals = _Normals()
    faces = _Faces()

    materials = _Materials()


    def open(self, filename):
        file = open(filename, "r")

        for line in file:
            parts = line.split(" ")
            if parts[0] == "mtllib":
                mtllib = _MaterialLib(self.materials)
                mtllib.load("/".join(filename.split("/")[:-1]) + "/" + parts[1].strip())
            if parts[0] == "v":
                self.vertices.add(float(parts[1]), float(parts[2]), float(parts[3]))
            if parts[0] == "vn":
                self.normals.add(float(parts[1]), float(parts[2]), float(parts[3]))
            if parts[0] == "vt":
                self.texturecoords.add(float(parts[1]), float(parts[2]))
            if parts[0] == "f":
                self.faces.add(parts[1].split("/"), parts[2].split("/"), parts[3].split("/"))

    def getArray(self):
        return self.faces.getVertices()

    def getMaterial(self):
        return self.materials.materials.items()[0][1]