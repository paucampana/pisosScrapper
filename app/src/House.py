class House:
    def __init__(self, titulo = "", zona = "", precio = "", num_hab = "", num_bano = "", 
                 metro_q = "", num_planta = "", contacto = "", contacto_tel = "", 
                 contacto_extra = "", caracteristicas = "", extras = "", 
                 ubicacion = "",descripcion = "", images = "", referencia = "", url = ""):
        self.titulo = titulo
        self.zona = zona
        self.precio = precio
        self.num_hab = num_hab
        self.num_bano = num_bano
        self.metro_q = metro_q
        self.num_planta = num_planta
        self.contacto = contacto
        self.contacto_tel = contacto_tel
        self.contacto_extra = contacto_extra
        self.caracteristicas = caracteristicas
        self.extras = extras
        self.ubicacion = ubicacion
        self.descripcion = descripcion
        self.images = images
        self.referencia = referencia
        self.url = url


    def getData(self):
        return "ZONA: {0}\nPRECIO: {1}\nNUM_HAB: {2}\nNUM_BANO: {3}\nMETRO_Q: {4}\nNUM_PLANTA: {5}\nCONTACTO: {6}\nCONTACTO_TEL: {7}\nCONTACTO_EXTRA: {8}\nCARACTERISTICAS: {9}\nEXTRAS: {10}\nUBICACION: {11}\nDESCRIPCION: {12}\nIMAGES {13}\nREFERENCIA: {14}\nURL: {15}\n".format(
        self.zona, self.precio, self.num_hab, self.num_bano, self.metro_q,
        self.num_planta, self.contacto, self.contacto_tel, self.contacto_extra, self.caracteristicas, 
        self.extras, self.ubicacion, self.descripcion,  self.images, self.referencia, self.url);

    def getDataAsList(self):
        myList = []
        myList.append(self.zona)
        myList.append(self.precio)
        myList.append(self.num_hab)
        myList.append(self.num_bano)
        myList.append(self.metro_q)
        myList.append(self.num_planta)
        myList.append(self.ubicacion)
        myList.append(self.caracteristicas)
        myList.append(self.extras)
        myList.append(self.contacto)
        myList.append(self.contacto_tel)
        myList.append(self.contacto_extra)
        myList.append(self.descripcion)
        myList.append(self.images)
        myList.append(self.referencia)
        myList.append(self.url)
        return myList;

    

