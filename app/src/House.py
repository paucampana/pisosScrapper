class House:
    def __init__(self, mapHouse = {}):
        self.titulo = mapHouse["titulo"]
        self.zona = mapHouse["zona"]
        self.precio = mapHouse["precio"]
        self.num_hab = mapHouse["num_hab"]
        self.num_bano = mapHouse["num_bano"]
        self.metro_q = mapHouse["metro_q"]
        self.precio_m = mapHouse["precio_m"]
        self.description = mapHouse["description"]
        self.antic = mapHouse["antic"]
        self.conservacion = mapHouse["conservacion"]
        self.caracteristicas = mapHouse["caracteristicas"]
        self.url = mapHouse["url"]

    def getData(self):
        return "TITULO: {0}\ZONA: {1}\PRECIO: {2}\HABITACIONES: {3}\BANOS: {4}\nNUM_PLANTA: {5}\METROS_QUADRADOS: {6}\nPLANTA: {7}\nPRECIO_M_2: {8}\DESCRIPCION: {9}\nESTADO: {10}\CARACTERISTICAS: {11}\nURL: {12}\n".format(
        self.titulo, self.zona, self.precio, self.num_hab, self.num_bano,
        self.metro_q, self.precio_m, self.description, self.antic, self.conservacion, 
        self.caracteristicas, self.url);

    def getDataAsList(self):
        myList = []
        myList.append(self.titulo)
        myList.append(self.zona)
        myList.append(self.precio)
        myList.append(self.num_hab)
        myList.append(self.num_bano)
        myList.append(self.metro_q)
        myList.append(self.precio_m)
        myList.append(self.description)
        myList.append(self.antic)
        myList.append(self.conservacion)
        myList.append(self.caracteristicas)
        myList.append(self.url)
        return myList;

    

