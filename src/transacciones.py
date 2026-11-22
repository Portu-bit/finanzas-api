from .database import (
    DEFAULT_DB,
    crear_tabla_transacciones,
    insertar_transaccion,
    obtener_transacciones,
)
from .excepciones import (
    MontoNegativoError,
    SaldoInsuficienteError,
    TipoTransaccionInvalidaError,
)


class GestorFinanzas:
    def __init__(self, db=DEFAULT_DB):
        self.db = str(db)
        crear_tabla_transacciones(self.db)

    @staticmethod
    def _validar(monto, descripcion):
        if isinstance(monto, bool) or not isinstance(monto, (int, float)) or monto <= 0:
            raise MontoNegativoError("El monto debe ser un número mayor que cero.")
        if not isinstance(descripcion, str) or not descripcion.strip():
            raise TipoTransaccionInvalidaError("La descripción no puede estar vacía.")

    def agregar_ingreso(self, monto, descripcion):
        self._validar(monto, descripcion)
        return insertar_transaccion(
            "ingreso", descripcion.strip(), float(monto), db=self.db
        )

    def agregar_gasto(self, monto, descripcion):
        self._validar(monto, descripcion)
        if monto > self.obtener_balance():
            raise SaldoInsuficienteError(
                "Saldo insuficiente para realizar esta transacción."
            )
        return insertar_transaccion(
            "gasto", descripcion.strip(), float(monto), db=self.db
        )

    def obtener_transacciones(self):
        return obtener_transacciones(db=self.db)

    def obtener_balance(self):
        balance = 0.0
        for transaccion in self.obtener_transacciones():
            if transaccion["tipo"] == "ingreso":
                balance += transaccion["monto"]
            else:
                balance -= transaccion["monto"]
        return round(balance, 2)
