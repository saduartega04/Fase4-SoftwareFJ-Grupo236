# =====================================================================
# entidades.py
# Clase abstracta general del sistema y clase Cliente.
# Fase 4 - Programación 213023 - UNAD - Grupo 236
# =====================================================================

from abc import ABC, abstractmethod  # ABC permite crear clases abstractas
from datetime import datetime  # Para guardar la fecha de creación de cada entidad

from excepciones import DatoInvalidoError, ParametroFaltanteError  # Errores propios del sistema
from registro import registrar_evento  # Para guardar eventos en el log


class EntidadBase(ABC):  # Clase abstracta: no se puede crear un objeto directamente de ella
    """Representa cualquier elemento del sistema (cliente, servicio o reserva)."""

    _contadores = {}  # Atributo de clase: un contador por cada tipo de entidad (CLI, SRV, RES)

    def __init__(self, prefijo):  # El prefijo identifica el tipo de entidad (CLI, SRV, RES)
        EntidadBase._contadores[prefijo] = EntidadBase._contadores.get(prefijo, 0) + 1  # Suma uno al contador de ese tipo
        self._id = f"{prefijo}-{EntidadBase._contadores[prefijo]:03d}"  # Arma un código único, por ejemplo CLI-001
        self._fecha_creacion = datetime.now()  # Guarda la fecha y hora en que se creó

    @property
    def id(self):  # Permite leer el id sin poder cambiarlo desde afuera
        return self._id  # Devuelve el código único

    @abstractmethod
    def describir(self):  # Método abstracto: cada clase hija debe escribir su propia versión
        """Devuelve un texto que describe la entidad."""

    @staticmethod
    def validar_texto(valor, nombre_campo):  # Método de apoyo que usan las clases hijas
        """Revisa que un texto obligatorio no venga vacío ni con un tipo incorrecto."""
        if valor is None or (isinstance(valor, str) and valor.strip() == ""):  # Si no viene o viene vacío
            raise ParametroFaltanteError(nombre_campo)  # Lanza el error de parámetro faltante
        if not isinstance(valor, str):  # Si no es un texto
            raise DatoInvalidoError(f"El campo '{nombre_campo}' debe ser texto")  # Lanza error de dato inválido
        return valor.strip()  # Devuelve el texto sin espacios al inicio ni al final


class Cliente(EntidadBase):  # Cliente hereda de la clase abstracta EntidadBase
    """Cliente de Software FJ, con sus datos personales encapsulados."""

    def __init__(self, nombre, documento, correo, telefono):  # Datos que pide un cliente
        super().__init__("CLI")  # Llama al constructor de EntidadBase con el prefijo CLI
        self.nombre = nombre  # Usa el setter de abajo, que valida el nombre
        self.documento = documento  # Usa el setter, que valida el documento
        self.correo = correo  # Usa el setter, que valida el correo
        self.telefono = telefono  # Usa el setter, que valida el teléfono
        registrar_evento(f"Cliente registrado: {self.__nombre} ({self.id})")  # Deja constancia en el log

    # ----- nombre -----
    @property
    def nombre(self):  # Getter: permite leer el nombre
        return self.__nombre  # Atributo privado (doble guion bajo = encapsulado)

    @nombre.setter
    def nombre(self, valor):  # Setter: valida antes de guardar
        valor = self.validar_texto(valor, "nombre")  # Revisa que no esté vacío
        if any(caracter.isdigit() for caracter in valor):  # Si el nombre tiene algún número
            raise DatoInvalidoError("El nombre no puede contener números")  # Lo rechaza
        if len(valor) < 3:  # Si es demasiado corto
            raise DatoInvalidoError("El nombre debe tener al menos 3 caracteres")  # Lo rechaza
        self.__nombre = valor  # Si pasó las validaciones, lo guarda

    # ----- documento -----
    @property
    def documento(self):  # Getter del documento
        return self.__documento  # Devuelve el documento privado

    @documento.setter
    def documento(self, valor):  # Setter del documento
        valor = self.validar_texto(str(valor) if valor is not None else None, "documento")  # Lo pasa a texto y revisa que exista
        if not valor.isdigit():  # Si tiene letras o símbolos
            raise DatoInvalidoError("El documento solo puede contener números")  # Lo rechaza
        if not 6 <= len(valor) <= 10:  # Si no tiene entre 6 y 10 dígitos
            raise DatoInvalidoError("El documento debe tener entre 6 y 10 dígitos")  # Lo rechaza
        self.__documento = valor  # Lo guarda

    # ----- correo -----
    @property
    def correo(self):  # Getter del correo
        return self.__correo  # Devuelve el correo privado

    @correo.setter
    def correo(self, valor):  # Setter del correo
        valor = self.validar_texto(valor, "correo")  # Revisa que exista
        if "@" not in valor or "." not in valor.split("@")[-1]:  # Debe tener @ y un punto después de la @
            raise DatoInvalidoError(f"El correo '{valor}' no es válido")  # Lo rechaza
        self.__correo = valor.lower()  # Lo guarda en minúsculas

    # ----- teléfono -----
    @property
    def telefono(self):  # Getter del teléfono
        return self.__telefono  # Devuelve el teléfono privado

    @telefono.setter
    def telefono(self, valor):  # Setter del teléfono
        valor = self.validar_texto(str(valor) if valor is not None else None, "telefono")  # Lo pasa a texto y revisa que exista
        if not (valor.isdigit() and len(valor) == 10):  # En Colombia un celular tiene 10 dígitos
            raise DatoInvalidoError("El teléfono debe tener 10 dígitos numéricos")  # Lo rechaza
        self.__telefono = valor  # Lo guarda

    def describir(self):  # Implementa el método abstracto de EntidadBase
        return f"Cliente {self.id}: {self.__nombre} | Doc. {self.__documento} | {self.__correo}"  # Texto descriptivo
