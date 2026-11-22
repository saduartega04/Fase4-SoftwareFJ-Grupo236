# =====================================================================
# main.py
# Programa principal: simula operaciones válidas e inválidas del sistema
# Software FJ y demuestra que la aplicación nunca se detiene por un error.
# Fase 4 - Programación 213023 - UNAD - Grupo 236
# =====================================================================

from entidades import Cliente  # Clase Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria  # Los tres servicios
from reserva import Reserva  # Clase Reserva
from excepciones import SoftwareFJError  # Clase base de todos los errores propios
from registro import registrar_evento, registrar_error, ARCHIVO_LOG  # Funciones del log

# Listas en memoria (el sistema no usa base de datos)
clientes = []  # Lista de clientes registrados
servicios = []  # Lista de servicios disponibles
reservas = []  # Lista de reservas creadas

resultados = {"exitosas": 0, "fallidas": 0}  # Contador de operaciones


def ejecutar_operacion(numero, descripcion, accion):
    """Ejecuta una operación y controla cualquier error para que el
    programa siga funcionando. Usa try / except / else / finally."""
    print(f"\n[{numero:02d}] {descripcion}")  # Muestra qué operación se va a hacer
    try:
        resultado = accion()  # Ejecuta la operación (una función sin parámetros)
    except SoftwareFJError as error:  # Errores propios del sistema (los esperados)
        resultados["fallidas"] += 1  # Cuenta la operación fallida
        print(f"     ✗ Error controlado: {error}")  # Avisa en pantalla
        if error.__cause__:  # Si el error fue encadenado (raise ... from ...)
            print(f"       Causa original: {error.__cause__}")  # Muestra también la causa
        registrar_error(f"Operación {numero:02d} fallida ({descripcion})", error)  # Lo guarda en el log
    except Exception as error:  # Cualquier otro error inesperado de Python
        resultados["fallidas"] += 1  # También cuenta como fallida
        print(f"     ✗ Error inesperado controlado: {type(error).__name__}: {error}")  # Avisa en pantalla
        registrar_error(f"Operación {numero:02d} con error inesperado", error)  # Lo guarda en el log
    else:  # Solo entra aquí si NO hubo error
        resultados["exitosas"] += 1  # Cuenta la operación exitosa
        print(f"     ✓ {resultado}")  # Muestra el resultado
    finally:  # Se ejecuta siempre
        registrar_evento(f"Operación {numero:02d} terminada")  # Deja constancia en el log


# ----- Funciones de apoyo para no repetir código -----
def registrar_cliente(*datos):  # Crea un cliente y lo agrega a la lista
    cliente = Cliente(*datos)  # Si algún dato es inválido, aquí se lanza el error
    clientes.append(cliente)  # Lo guarda en la lista
    return cliente.describir()  # Devuelve su descripción


def agregar_servicio(clase, *datos):  # Crea cualquier servicio (polimorfismo) y lo agrega
    servicio = clase(*datos)  # La clase puede ser ReservaSala, AlquilerEquipo o Asesoria
    servicios.append(servicio)  # Lo guarda en la lista
    return servicio.describir()  # Devuelve su descripción


def crear_reserva(cliente, servicio, duracion):  # Crea una reserva y la agrega
    reserva = Reserva(cliente, servicio, duracion)  # Si algo no cuadra, aquí se lanza el error
    reservas.append(reserva)  # La guarda en la lista
    return reserva.describir()  # Devuelve su descripción


def confirmar_y_procesar(reserva, impuesto=0.0, descuento=0.0):  # Confirma y cobra una reserva
    reserva.confirmar()  # Primero la confirma
    total = reserva.procesar(impuesto, descuento)  # Luego calcula el cobro
    return f"Reserva {reserva.id} procesada. Total a pagar: ${total:,.2f}"


def main():
    registrar_evento("===== Inicio de la simulación de Software FJ =====")  # Marca el inicio en el log
    print("=" * 60)
    print("   SOFTWARE FJ - Sistema de clientes, servicios y reservas")
    print("=" * 60)

    # --- Clientes ---
    ejecutar_operacion(1, "Registrar cliente válido (Ana Gómez)",
                       lambda: registrar_cliente("Ana Gómez", "1023456789", "ana.gomez@correo.com", "3001234567"))
    ejecutar_operacion(2, "Registrar cliente válido (Carlos Ruiz)",
                       lambda: registrar_cliente("Carlos Ruiz", "79845612", "carlos.ruiz@correo.com", "3157654321"))
    ejecutar_operacion(3, "Registrar cliente con correo inválido",
                       lambda: registrar_cliente("Luisa Pérez", "52147896", "luisa.correo.com", "3209876543"))
    ejecutar_operacion(4, "Registrar cliente sin nombre (parámetro faltante)",
                       lambda: registrar_cliente("", "1098765432", "sin.nombre@correo.com", "3112223344"))
    ejecutar_operacion(5, "Registrar cliente con documento con letras",
                       lambda: registrar_cliente("Pedro Díaz", "12AB345", "pedro@correo.com", "3001112233"))

    # --- Servicios ---
    ejecutar_operacion(6, "Crear servicio: sala de reuniones",
                       lambda: agregar_servicio(ReservaSala, "Sala Innovación", 50000, 12))
    ejecutar_operacion(7, "Crear servicio: alquiler de portátiles",
                       lambda: agregar_servicio(AlquilerEquipo, "Portátil Lenovo", 35000, 3))
    ejecutar_operacion(8, "Crear servicio: asesoría avanzada",
                       lambda: agregar_servicio(Asesoria, "Asesoría en Python", 80000, "avanzado"))
    ejecutar_operacion(9, "Crear servicio con precio negativo",
                       lambda: agregar_servicio(ReservaSala, "Sala Fantasma", -20000, 10))
    ejecutar_operacion(10, "Crear asesoría con nivel inexistente",
                       lambda: agregar_servicio(Asesoria, "Asesoría en Java", 70000, "experto"))

    ana, carlos = clientes[0], clientes[1]  # Los dos clientes válidos
    sala, equipo, asesoria = servicios[0], servicios[1], servicios[2]  # Los tres servicios válidos

    # --- Reservas ---
    ejecutar_operacion(11, "Reservar sala 3 horas para Ana",
                       lambda: crear_reserva(ana, sala, 3))
    ejecutar_operacion(12, "Confirmar y procesar reserva de Ana con IVA 19 %",
                       lambda: confirmar_y_procesar(reservas[0], 0.19))
    ejecutar_operacion(13, "Reservar portátiles 10 días para Carlos",
                       lambda: crear_reserva(carlos, equipo, 10))
    ejecutar_operacion(14, "Confirmar reserva de portátiles de Carlos",
                       lambda: (reservas[1].confirmar(), reservas[1].describir())[1])
    ejecutar_operacion(15, "Ana intenta reservar los portátiles ya ocupados",
                       lambda: confirmar_y_procesar(Reserva(ana, equipo, 2)))
    ejecutar_operacion(16, "Reservar la sala por 12 horas (excede el máximo)",
                       lambda: crear_reserva(carlos, sala, 12))
    ejecutar_operacion(17, "Reservar con un cliente que no existe",
                       lambda: crear_reserva("Cliente desconocido", asesoria, 2))
    ejecutar_operacion(18, "Procesar portátiles de Carlos con descuento del 150 %",
                       lambda: reservas[1].procesar(0.19, 1.5))
    ejecutar_operacion(19, "Procesar portátiles de Carlos con IVA y 10 % de descuento",
                       lambda: f"Total a pagar: ${reservas[1].procesar(0.19, 0.10):,.2f}")
    ejecutar_operacion(20, "Reservar asesoría 2 horas para Carlos y cancelarla",
                       lambda: (crear_reserva(carlos, asesoria, 2), reservas[-1].cancelar(), reservas[-1].describir())[2])
    ejecutar_operacion(21, "Cancelar otra vez la misma reserva (operación no permitida)",
                       lambda: reservas[-1].cancelar())

    # --- Resumen ---
    print("\n" + "=" * 60)
    print(f"Operaciones exitosas: {resultados['exitosas']}")
    print(f"Operaciones con error controlado: {resultados['fallidas']}")
    print(f"El programa terminó sin detenerse. Revise el archivo '{ARCHIVO_LOG}'.")
    print("=" * 60)
    registrar_evento(f"===== Fin de la simulación: {resultados['exitosas']} exitosas, "
                     f"{resultados['fallidas']} fallidas =====")


if __name__ == "__main__":  # Solo se ejecuta si se corre este archivo directamente
    main()  # Arranca el programa
