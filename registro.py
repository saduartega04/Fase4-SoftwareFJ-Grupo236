# =====================================================================
# registro.py
# Manejo del archivo de logs del sistema Software FJ.
# Fase 4 - Programación 213023 - UNAD - Grupo 236
# =====================================================================
# Aquí se configura el archivo "softwarefj.log", donde quedan guardados
# todos los eventos importantes (INFO) y todos los errores (ERROR) que
# ocurren mientras el programa se ejecuta.
# =====================================================================

import logging  # Módulo de Python para escribir registros (logs)

ARCHIVO_LOG = "softwarefj.log"  # Nombre del archivo donde se guardan los registros

# Se crea un "logger" propio del sistema, identificado con el nombre "SoftwareFJ"
_logger = logging.getLogger("SoftwareFJ")
_logger.setLevel(logging.INFO)  # Guarda desde mensajes informativos (INFO) hacia arriba (WARNING, ERROR)

if not _logger.handlers:  # Evita configurar el archivo dos veces si este módulo se importa varias veces
    _manejador = logging.FileHandler(ARCHIVO_LOG, mode="a", encoding="utf-8")  # "a" = agrega al final sin borrar lo anterior
    _formato = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s",  # Fecha y hora | nivel | mensaje
                                 datefmt="%Y-%m-%d %H:%M:%S")  # Formato de la fecha: 2026-11-06 19:55:00
    _manejador.setFormatter(_formato)  # Le aplica el formato al archivo
    _logger.addHandler(_manejador)  # Conecta el archivo con el logger


def registrar_evento(mensaje):
    """Guarda en el log un evento normal (por ejemplo, 'Cliente registrado')."""
    _logger.info(mensaje)  # Escribe el mensaje con nivel INFO


def registrar_advertencia(mensaje):
    """Guarda en el log algo que no es un error pero merece atención."""
    _logger.warning(mensaje)  # Escribe el mensaje con nivel WARNING


def registrar_error(mensaje, excepcion=None):
    """Guarda en el log un error. Si se pasa la excepción, también guarda
    su tipo y, si fue encadenada, la causa original."""
    if excepcion is None:  # Si no se pasó ninguna excepción
        _logger.error(mensaje)  # Solo guarda el mensaje
        return  # Termina la función aquí

    detalle = f"{mensaje} -> {type(excepcion).__name__}: {excepcion}"  # Agrega el tipo de error y su texto
    if excepcion.__cause__ is not None:  # Si el error viene de otro (raise ... from ...)
        causa = excepcion.__cause__  # Toma el error original
        detalle += f" | Causa original: {type(causa).__name__}: {causa}"  # Lo agrega al mensaje
    _logger.error(detalle)  # Guarda todo con nivel ERROR


# ---------------------------------------------------------------------
# Prueba rápida: solo se ejecuta si se corre este archivo directamente
# (python registro.py). Cuando otro archivo lo importa, no se ejecuta.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    from excepciones import DatoInvalidoError, CalculoInconsistenteError  # Trae dos excepciones para probar

    registrar_evento("Prueba del módulo de registro iniciada")  # Evento normal

    # try / except / else: el else se ejecuta solo si NO hubo error
    try:
        precio = float("150000")  # Convierte un texto válido a número
    except ValueError as error:
        registrar_error("No se pudo convertir el precio", error)
    else:
        registrar_evento(f"Precio convertido correctamente: {precio}")  # Se ejecuta porque no hubo error

    # Encadenamiento de excepciones (raise ... from ...) + try / except / finally
    try:
        try:
            float("abc")  # Esto falla con ValueError
        except ValueError as error_original:
            # Se convierte en un error propio, pero se conserva el original como causa
            raise DatoInvalidoError("El precio debe ser un número") from error_original
    except DatoInvalidoError as error:
        registrar_error("Error de validación", error)  # Queda en el log con su causa original
        print("Error controlado:", error)  # El programa no se detiene
    finally:
        registrar_evento("Fin de la prueba de encadenamiento")  # El finally se ejecuta siempre

    # Un error personalizado lanzado directamente
    try:
        raise CalculoInconsistenteError("El total no puede ser negativo")
    except CalculoInconsistenteError as error:
        registrar_error("Error de cálculo", error)
        print("Error controlado:", error)

    print(f"Prueba terminada. Revisa el archivo {ARCHIVO_LOG}")  # Mensaje final
