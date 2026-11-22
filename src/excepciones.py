class MontoNegativoError(ValueError):
    """Raised when a transaction amount is not positive."""


class SaldoInsuficienteError(ValueError):
    """Raised when an expense exceeds the available balance."""


class TipoTransaccionInvalidaError(ValueError):
    """Raised when a transaction description or type is invalid."""
