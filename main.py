from fastapi import FastAPI
import sys
sys.path.append('..')  # le dice a Python que busque un nivel arriba

from src.transacciones import GestorFinanzas
from src.database import crear_tabla_transacciones
from pydantic import BaseModel

app = FastAPI()
crear_tabla_transacciones()  # Asegura que la tabla exista al iniciar la aplicación
gestor = GestorFinanzas()  # Inicializa el gestor para asegurarse de que la tabla se cree

class Transaccion(BaseModel):
    descripcion: str
    monto: float
    tipo: str  # 'ingreso' o 'gasto'

@app.post("/transacciones/ingreso")
def agregar_ingreso(transaccion: Transaccion):
    gestor.agregar_ingreso(transaccion.monto, transaccion.descripcion)
    return {"mensaje": "Ingreso agregado exitosamente"}

@app.post("/transacciones/gasto")
def agregar_gasto(transaccion: Transaccion):
    gestor.agregar_gasto(transaccion.monto, transaccion.descripcion)
    return {"mensaje": "Gasto agregado exitosamente"}

@app.get("/transacciones/")
def obtener_transacciones():
    transacciones = gestor.obtener_transacciones()
    return {"transacciones": transacciones}

@app.get("/balance/")
def obtener_balance():
    balance = gestor.obtener_balance()
    return {"balance": balance}

if __name__ == "__main__":
    pass



