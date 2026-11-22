# =====================================================================
# servicios.py
# Clase abstracta Servicio y sus tres servicios especializados.
# Fase 4 - Programación 213023 - UNAD - Grupo 236
# =====================================================================

from abc import abstractmethod  # Para marcar los métodos que cada hijo debe implementar

from entidades import EntidadBase  # Clase abstracta general del sistema
from excepciones import DatoInvalidoError, CalculoInconsistenteError  # Errores propios
from registro import registrar_evento  # Para guardar eventos en el log


class Servicio(EntidadBase):  # Clase abstracta: hereda de EntidadBase y no implementa todos sus métodos
    """Servicio general que ofrece Software FJ."""

    def __init__(self, nombre, precio_base):  # Todo servicio tiene un nombre y un precio base
        super().__init__("SRV")  # Llama al constructor de EntidadBase con el prefijo SRV
        self.nombre = self.validar_texto(nombre, "nombre del servicio")  # Valida que el nombre exista
        if not isinstance(precio_base, (int, float)) or precio_base <= 0:  # El precio debe ser un número positivo
            raise DatoInvalidoError("El precio base debe ser un número mayor que cero")  # Si no, lo rechaza
        self.precio_base = precio_base  # Guarda el precio
        self.disponible = True  # Todo servicio nuevo empieza disponible

    @abstractmethod
    def calcular_costo(self, duracion):  # Cada servicio calcula su costo a su manera
        """Devuelve el costo del servicio según la duración."""

    @abstractmethod
    def validar_parametros(self, duracion):  # Cada servicio tiene sus propios límites de duración
        """Lanza un error si la duración no es válida para este servicio."""

    def calcular_costo_total(self, duracion, impuesto=0.0, descuento=0.0):
        """Método sobrecargado (con parámetros opcionales). Se puede llamar:
        - calcular_costo_total(3)                -> solo el costo
        - calcular_costo_total(3, 0.19)          -> costo con impuesto (IVA 19 %)
        - calcular_costo_total(3, 0.19, 0.10)    -> costo con impuesto y descuento del 10 %"""
        if not 0 <= impuesto <= 1:  # El impuesto debe estar entre 0 % y 100 %
            raise CalculoInconsistenteError(f"Impuesto fuera de rango: {impuesto}")  # Si no, el cálculo no tiene sentido
        if not 0 <= descuento < 1:  # El descuento debe estar entre 0 % y menos del 100 %
            raise CalculoInconsistenteError(f"Descuento fuera de rango: {descuento}")  # Si no, lo rechaza
        subtotal = self.calcular_costo(duracion)  # Polimorfismo: usa el cálculo propio de cada hijo
        total = subtotal * (1 - descuento) * (1 + impuesto)  # Aplica primero el descuento y luego el impuesto
        if total < 0:  # Revisión final de seguridad
            raise CalculoInconsistenteError("El total calculado es negativo")  # Nunca debería pasar
        return round(total, 2)  # Devuelve el total con dos decimales


class ReservaSala(Servicio):  # Servicio 1: reserva de salas
    """Reserva de una sala de reuniones, cobrada por hora."""

    MAX_HORAS = 8  # Una sala se puede reservar máximo 8 horas seguidas

    def __init__(self, nombre, precio_hora, capacidad):  # Además del nombre y el precio, tiene capacidad
        super().__init__(nombre, precio_hora)  # Llama al constructor de Servicio
        if not isinstance(capacidad, int) or capacidad <= 0:  # La capacidad debe ser un entero positivo
            raise DatoInvalidoError("La capacidad de la sala debe ser un entero mayor que cero")  # Si no, lo rechaza
        self.capacidad = capacidad  # Guarda la capacidad
        registrar_evento(f"Servicio creado: {self.describir()}")  # Deja constancia en el log

    def validar_parametros(self, duracion):  # Sobrescribe el método abstracto
        if not isinstance(duracion, (int, float)) or not 0 < duracion <= self.MAX_HORAS:  # Entre 0 y 8 horas
            raise DatoInvalidoError(f"La sala se reserva entre 1 y {self.MAX_HORAS} horas (se pidió {duracion})")

    def calcular_costo(self, duracion):  # Sobrescribe el método abstracto
        self.validar_parametros(duracion)  # Primero valida la duración
        costo = self.precio_base * duracion  # Precio por hora por número de horas
        if self.capacidad > 20:  # Las salas grandes tienen un recargo del 15 %
            costo *= 1.15  # Aplica el recargo
        return costo  # Devuelve el costo

    def describir(self):  # Sobrescribe el método abstracto
        return f"Sala '{self.nombre}' ({self.capacidad} personas) - ${self.precio_base:,.0f}/hora"


class AlquilerEquipo(Servicio):  # Servicio 2: alquiler de equipos
    """Alquiler de equipos (portátiles, proyectores...), cobrado por día y por unidad."""

    MAX_DIAS = 30  # Un equipo se alquila máximo 30 días

    def __init__(self, nombre, precio_dia, cantidad):  # Además tiene la cantidad de unidades
        super().__init__(nombre, precio_dia)  # Llama al constructor de Servicio
        if not isinstance(cantidad, int) or cantidad <= 0:  # La cantidad debe ser un entero positivo
            raise DatoInvalidoError("La cantidad de equipos debe ser un entero mayor que cero")  # Si no, lo rechaza
        self.cantidad = cantidad  # Guarda la cantidad
        registrar_evento(f"Servicio creado: {self.describir()}")  # Deja constancia en el log

    def validar_parametros(self, duracion):  # Sobrescribe el método abstracto
        if not isinstance(duracion, int) or not 1 <= duracion <= self.MAX_DIAS:  # Días enteros entre 1 y 30
            raise DatoInvalidoError(f"El alquiler es por días enteros entre 1 y {self.MAX_DIAS} (se pidió {duracion})")

    def calcular_costo(self, duracion):  # Sobrescribe el método abstracto
        self.validar_parametros(duracion)  # Primero valida la duración
        costo = self.precio_base * duracion * self.cantidad  # Precio por día por días por unidades
        if duracion >= 7:  # Si se alquila una semana o más, tiene 10 % de descuento
            costo *= 0.90  # Aplica el descuento
        return costo  # Devuelve el costo

    def describir(self):  # Sobrescribe el método abstracto
        return f"Equipo '{self.nombre}' x{self.cantidad} - ${self.precio_base:,.0f}/día"


class Asesoria(Servicio):  # Servicio 3: asesorías especializadas
    """Asesoría con un especialista, cobrada por hora según el nivel."""

    NIVELES = {"basico": 1.0, "avanzado": 1.5}  # El nivel avanzado cuesta 50 % más

    def __init__(self, nombre, precio_hora, nivel):  # Además tiene el nivel de la asesoría
        super().__init__(nombre, precio_hora)  # Llama al constructor de Servicio
        if nivel not in self.NIVELES:  # El nivel debe ser uno de los permitidos
            raise DatoInvalidoError(f"Nivel '{nivel}' no válido. Use: {', '.join(self.NIVELES)}")  # Si no, lo rechaza
        self.nivel = nivel  # Guarda el nivel
        registrar_evento(f"Servicio creado: {self.describir()}")  # Deja constancia en el log

    def validar_parametros(self, duracion):  # Sobrescribe el método abstracto
        if not isinstance(duracion, (int, float)) or not 1 <= duracion <= 4:  # Una asesoría dura entre 1 y 4 horas
            raise DatoInvalidoError(f"La asesoría dura entre 1 y 4 horas (se pidió {duracion})")

    def calcular_costo(self, duracion):  # Sobrescribe el método abstracto
        self.validar_parametros(duracion)  # Primero valida la duración
        return self.precio_base * duracion * self.NIVELES[self.nivel]  # Precio por horas por el factor del nivel

    def describir(self):  # Sobrescribe el método abstracto
        return f"Asesoría '{self.nombre}' (nivel {self.nivel}) - ${self.precio_base:,.0f}/hora"
