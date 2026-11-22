from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.excepciones import (
    MontoNegativoError,
    SaldoInsuficienteError,
    TipoTransaccionInvalidaError,
)
from src.transacciones import GestorFinanzas

app = FastAPI(
    title="Finanzas API",
    description="API REST para registrar ingresos, gastos y consultar el balance.",
    version="1.0.0",
)
gestor = GestorFinanzas()


class TransaccionEntrada(BaseModel):
    descripcion: str = Field(min_length=1, max_length=200)
    monto: float = Field(gt=0, allow_inf_nan=False)


@app.get("/", tags=["general"])
def inicio():
    return {"mensaje": "Finanzas API está funcionando", "docs": "/docs"}


@app.post("/transacciones/ingreso", status_code=201, tags=["transacciones"])
def agregar_ingreso(transaccion: TransaccionEntrada):
    try:
        transaction_id = gestor.agregar_ingreso(
            transaccion.monto, transaccion.descripcion
        )
        return {"mensaje": "Ingreso agregado exitosamente", "id": transaction_id}
    except (MontoNegativoError, TipoTransaccionInvalidaError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/transacciones/gasto", status_code=201, tags=["transacciones"])
def agregar_gasto(transaccion: TransaccionEntrada):
    try:
        transaction_id = gestor.agregar_gasto(
            transaccion.monto, transaccion.descripcion
        )
        return {"mensaje": "Gasto agregado exitosamente", "id": transaction_id}
    except SaldoInsuficienteError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except (MontoNegativoError, TipoTransaccionInvalidaError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/transacciones/", tags=["transacciones"])
def listar_transacciones():
    return {"transacciones": gestor.obtener_transacciones()}


@app.get("/balance/", tags=["balance"])
def obtener_balance():
    return {"balance": gestor.obtener_balance()}
