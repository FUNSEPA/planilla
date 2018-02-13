from num2words import num2words


class Empleado(object):
    nombre = ''
    codigo = ''
    correo = ''
    cuenta = ''
    primera = 0.0
    decreto = 0.0
    descuentos = 0.0
    asdeco = 0.0
    igss = 0.0
    salario = 0.0
    total_descuentos = 0.0
    depositar = 0.0

    def __init__(self, quincena=1, datos=[], *args, **kwargs):
        if quincena == 1:
            self.crear_primera(datos)
        elif quincena == 2:
            self.crear_segunda(datos)
        elif quincena == 3:
            self.crear_bono(datos)
        elif quincena == 4:
            self.crear_aguinaldo(datos)

    def __repr__(self):
        return self.nombre

    def crear_primera(self, datos):
        self.nombre = datos[1].value
        self.codigo = datos[0].value
        self.correo = datos[2].value
        self.cuenta = datos[5].value
        self.primera = float(datos[6].value)
        self.decreto = float(datos[7].value)
        self.descuentos = float(datos[9].value)
        self.igss = float(datos[10].value)
        self.asdeco = float(datos[11].value)
        self.salario = self.primera + self.decreto
        self.total_descuentos = self.descuentos + self.asdeco + self.igss
        self.depositar = round(float(self.salario - self.total_descuentos), 2)

    def crear_segunda(self, datos):
        self.nombre = datos[1].value
        self.codigo = datos[0].value
        self.correo = datos[2].value
        self.cuenta = datos[4].value
        self.sueldo = float(datos[5].value)

        self.bonificacion = float(datos[6].value)
        self.otros = float(datos[7].value)
        self.quincena = float(datos[9].value)
        self.igss2 = float(datos[10].value)
        self.isr = float(datos[11].value)
        self.boleto = float(datos[12].value)
        self.asdeco2 = float(datos[13].value)
        self.descuentos = float(datos[14].value)

        self.devengado = self.sueldo + self.bonificacion + self.otros
        self.total_descontado = self.quincena + self.igss2 + self.isr + self.boleto + self.asdeco2 + self.descuentos
        self.depositar2 = self.devengado - self.total_descontado

    def crear_bono(self, datos):
        self.nombre = datos[1].value
        self.codigo = datos[0].value
        self.correo = datos[2].value
        self.cuenta = datos[3].value
        self.bono = round(datos[20].value, 2)
        self.letras = num2words(self.bono, lang='es')

    def crear_aguinaldo(self, datos):
        self.nombre = datos[1].value
        self.codigo = datos[0].value
        self.correo = datos[2].value
        self.cuenta = datos[3].value
        self.aguinaldo = round(datos[20].value, 2)
        self.letras = num2words(self.aguinaldo, lang='es')
