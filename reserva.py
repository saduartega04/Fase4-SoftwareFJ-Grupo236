# =====================================================================
# reserva.py
# Clase Reserva: une un cliente, un servicio y una duración.
# Fase 4 - Programación 213023 - UNAD - Grupo 236
# =====================================================================

from entidades import EntidadBase, Cliente  # Clase abstracta general y Cliente
from servicios import Servicio  # Clase abstracta de los servicios
from excepciones import (  # Errores propios que puede lanzar una reserva
    ReservaInvalidaError, OperacionNoPermitidaError,
    ServicioNoDisponibleError, DatoInvalidoError, CalculoInconsistenteError,
)
from registro import registrar_evento, registrar_error  # Para guardar en el log


class Reserva(EntidadBase):  # Reserva hereda de la clase abstracta EntidadBase
    """Reserva de un servicio por parte de un cliente."""

    ESTADOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")  # Estados posibles de una reserva

    def __init__(self, cliente, servicio, duracion):  # Una reserva necesita cliente, servicio y duración
        if not isinstance(cliente, Cliente):  # El cliente debe ser un objeto Cliente válido
            raise ReservaInvalidaError("La reserva necesita un cliente válido")  # Si no, la rechaza
        if not isinstance(servicio, Servicio):  # El servicio debe ser un objeto Servicio
            raise ReservaInvalidaError("La reserva necesita un servicio válido")  # Si no, la rechaza
        try:
            servicio.validar_parametros(duracion)  # Cada servicio revisa si la duración le sirve (polimorfismo)
        except DatoInvalidoError as error:  # Si la duración no sirve...
            raise ReservaInvalidaError(f"Duración no válida para {servicio.nombre}") from error  # ...encadena el error
        super().__init__("RES")  # Si todo está bien, crea la entidad con prefijo RES
        self.cliente = cliente  # Guarda el cliente
        self.servicio = servicio  # Guarda el servicio
        self.duracion = duracion  # Guarda la duración
        self.estado = "PENDIENTE"  # Toda reserva nueva empieza pendiente
        self.total = 0  # El total se calcula al procesarla
        registrar_evento(f"Reserva creada: {self.describir()}")  # Deja constancia en el log

    def confirmar(self):
        """Confirma la reserva y deja el servicio ocupado."""
        if self.estado != "PENDIENTE":  # Solo se confirma una reserva pendiente
            raise OperacionNoPermitidaError(f"No se puede confirmar la reserva {self.id}: está {self.estado}")
        if not self.servicio.disponible:  # Si otro cliente ya ocupó el servicio
            raise ServicioNoDisponibleError(self.servicio.nombre)  # No se puede confirmar
        self.servicio.disponible = False  # Marca el servicio como ocupado
        self.estado = "CONFIRMADA"  # Cambia el estado
        registrar_evento(f"Reserva {self.id} confirmada")  # Deja constancia en el log

    def cancelar(self):
        """Cancela la reserva y libera el servicio."""
        if self.estado in ("CANCELADA", "PROCESADA"):  # No se cancela algo ya cancelado o ya cobrado
            raise OperacionNoPermitidaError(f"No se puede cancelar la reserva {self.id}: está {self.estado}")
        if self.estado == "CONFIRMADA":  # Si estaba confirmada, el servicio estaba ocupado
            self.servicio.disponible = True  # Lo libera para otros clientes
        self.estado = "CANCELADA"  # Cambia el estado
        registrar_evento(f"Reserva {self.id} cancelada")  # Deja constancia en el log

    def procesar(self, impuesto=0.0, descuento=0.0):
        """Calcula el cobro de la reserva. Usa try / except / else / finally."""
        if self.estado != "CONFIRMADA":  # Solo se cobra una reserva confirmada
            raise OperacionNoPermitidaError(f"La reserva {self.id} debe estar CONFIRMADA para procesarse (está {self.estado})")
        try:
            total = self.servicio.calcular_costo_total(self.duracion, impuesto, descuento)  # Usa el método sobrecargado
        except CalculoInconsistenteError as error:  # Si el cálculo no tiene sentido...
            registrar_error(f"Fallo al procesar la reserva {self.id}", error)  # ...lo guarda en el log
            raise ReservaInvalidaError(f"No se pudo procesar la reserva {self.id}") from error  # ...y lo encadena
        else:  # Solo entra aquí si el cálculo salió bien
            self.total = total  # Guarda el total
            self.estado = "PROCESADA"  # Cambia el estado
            self.servicio.disponible = True  # El servicio queda libre después de usarse
            registrar_evento(f"Reserva {self.id} procesada. Total: ${total:,.2f}")  # Deja constancia en el log
            return total  # Devuelve el total cobrado
        finally:  # Se ejecuta siempre, haya error o no
            registrar_evento(f"Intento de procesamiento de la reserva {self.id} finalizado")

    def describir(self):  # Implementa el método abstracto de EntidadBase
        return (f"Reserva {self.id}: {self.cliente.nombre} -> {self.servicio.nombre} "
                f"| duración {self.duracion} | estado {self.estado}")
