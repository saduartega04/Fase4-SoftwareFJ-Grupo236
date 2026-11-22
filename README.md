# Fase4-SoftwareFJ-Grupo236

Sistema integral de gestión de clientes, servicios y reservas para la empresa **Software FJ**, desarrollado en Python con programación orientada a objetos y manejo avanzado de excepciones. No usa base de datos: la información se maneja con objetos y listas en memoria, y los eventos y errores se guardan en un archivo de logs.

**Curso:** Programación (213023) – UNAD
**Actividad:** Fase 4 – Componente práctico – Prácticas simuladas
**Grupo:** 236

## Integrantes

| Nombre | Usuario GitHub | Aporte |
|---|---|---|
| William Augusto Mendoza R | @wamendozar | Repositorio, excepciones, logs, clases y simulaciones |

## Estructura del proyecto

| Archivo | Contenido |
|---|---|
| `excepciones.py` | Excepciones personalizadas (`SoftwareFJError` y 6 errores hijos) |
| `registro.py` | Configuración del archivo de logs `softwarefj.log` |
| `entidades.py` | Clase abstracta `EntidadBase` y clase `Cliente` con datos encapsulados y validados |
| `servicios.py` | Clase abstracta `Servicio` y los servicios `ReservaSala`, `AlquilerEquipo` y `Asesoria` |
| `reserva.py` | Clase `Reserva` (confirmar, cancelar y procesar) |
| `main.py` | Programa principal con 21 operaciones simuladas, válidas e inválidas |

## Conceptos aplicados

- **Abstracción:** `EntidadBase` y `Servicio` son clases abstractas (`ABC`, `@abstractmethod`).
- **Herencia y polimorfismo:** los tres servicios sobrescriben `calcular_costo()`, `validar_parametros()` y `describir()`.
- **Encapsulación:** los datos del cliente son atributos privados con `@property` y validación en cada setter.
- **Sobrecarga:** `calcular_costo_total(duracion, impuesto=0, descuento=0)` se puede llamar con 1, 2 o 3 parámetros.
- **Excepciones:** excepciones personalizadas, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from ...`.
- **Logs:** todos los eventos (INFO) y errores (ERROR) quedan en `softwarefj.log` con fecha y hora.

## Cómo ejecutarlo

Requiere Python 3.8 o superior. No necesita librerías externas.

```bash
python main.py
```

Al terminar se muestra un resumen en pantalla y se crea el archivo `softwarefj.log`.
