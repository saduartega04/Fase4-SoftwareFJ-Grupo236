# =====================================================================
# excepciones.py
# Excepciones personalizadas del sistema Software FJ.
# Fase 4 - Programación 213023 - UNAD - Grupo 236
# =====================================================================
# Todas las excepciones del sistema heredan de SoftwareFJError.
# Así el programa principal puede atrapar cualquier error propio con un
# solo "except SoftwareFJError" y seguir funcionando sin detenerse.
# =====================================================================


class SoftwareFJError(Exception):  # Clase base: hereda de Exception, la excepción general de Python
    """Error general del sistema Software FJ."""

    def __init__(self, mensaje, codigo="SFJ-000"):  # Recibe el mensaje del error y un código para identificarlo
        super().__init__(mensaje)  # Le pasa el mensaje a la clase Exception para que funcione como un error normal
        self.mensaje = mensaje  # Guarda el mensaje para poder mostrarlo después
        self.codigo = codigo  # Guarda el código del error (sirve para buscarlo rápido en el log)

    def __str__(self):  # Define cómo se ve el error cuando se imprime
        return f"[{self.codigo}] {self.mensaje}"  # Ejemplo: [SFJ-001] El nombre no puede estar vacío


class DatoInvalidoError(SoftwareFJError):  # Hija de SoftwareFJError
    """Se lanza cuando un dato tiene un formato o un valor incorrecto
    (por ejemplo, un correo sin @ o un documento con letras)."""

    def __init__(self, mensaje):  # Solo pide el mensaje
        super().__init__(mensaje, "SFJ-001")  # Le asigna su propio código


class ParametroFaltanteError(SoftwareFJError):  # Hija de SoftwareFJError
    """Se lanza cuando falta un dato obligatorio (vacío o None)."""

    def __init__(self, nombre_parametro):  # Recibe el nombre del dato que falta
        super().__init__(f"Falta el parámetro obligatorio: '{nombre_parametro}'", "SFJ-002")  # Arma el mensaje


class OperacionNoPermitidaError(SoftwareFJError):  # Hija de SoftwareFJError
    """Se lanza cuando se intenta una acción que no está permitida
    (por ejemplo, cancelar una reserva que ya estaba cancelada)."""

    def __init__(self, mensaje):  # Solo pide el mensaje
        super().__init__(mensaje, "SFJ-003")  # Le asigna su propio código


class ServicioNoDisponibleError(SoftwareFJError):  # Hija de SoftwareFJError
    """Se lanza cuando se intenta reservar un servicio que no está disponible."""

    def __init__(self, nombre_servicio):  # Recibe el nombre del servicio
        super().__init__(f"El servicio '{nombre_servicio}' no está disponible", "SFJ-004")  # Arma el mensaje


class ReservaInvalidaError(SoftwareFJError):  # Hija de SoftwareFJError
    """Se lanza cuando una reserva no se puede crear o procesar
    (por ejemplo, una duración negativa o un cliente inexistente)."""

    def __init__(self, mensaje):  # Solo pide el mensaje
        super().__init__(mensaje, "SFJ-005")  # Le asigna su propio código


class CalculoInconsistenteError(SoftwareFJError):  # Hija de SoftwareFJError
    """Se lanza cuando un cálculo de costos da un resultado que no tiene
    sentido (por ejemplo, un total negativo o un descuento mayor al 100 %)."""

    def __init__(self, mensaje):  # Solo pide el mensaje
        super().__init__(mensaje, "SFJ-006")  # Le asigna su propio código
