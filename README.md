# Finanzas API

API REST construida con **FastAPI** y **SQLite** para registrar ingresos y gastos personales, consultar transacciones y calcular el balance disponible.

## Funcionalidades

- Registrar ingresos.
- Registrar gastos, validando que exista saldo suficiente.
- Consultar el historial de transacciones.
- Consultar el balance actual.
- Validar montos y descripciones.
- Persistir datos en SQLite sin borrar registros al iniciar.

## Tecnologías

- Python 3.10+
- FastAPI
- Pydantic
- SQLite
- Uvicorn
- Pytest y HTTPX

## Instalación

Clona el repositorio y entra en su carpeta:

```bash
git clone https://github.com/Portu-bit/finanzas-api.git
cd finanzas-api
```

Crea y activa un entorno virtual (Windows):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Ejecutar la API

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

- Documentación interactiva: `http://127.0.0.1:8000/docs`
- Documentación alternativa: `http://127.0.0.1:8000/redoc`

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Estado de la API |
| POST | `/transacciones/ingreso` | Registrar ingreso |
| POST | `/transacciones/gasto` | Registrar gasto |
| GET | `/transacciones/` | Listar transacciones |
| GET | `/balance/` | Consultar balance |

Ejemplo de cuerpo JSON para registrar un ingreso:

```json
{
  "descripcion": "Salario",
  "monto": 1000
}
```

## Ejecutar pruebas

```bash
python -m pytest -v
```

Las pruebas usan bases de datos temporales, por lo que no modifican la base de datos de la aplicación.

## Base de datos

La aplicación utiliza `finanzas.db` en la raíz del proyecto. La inicialización usa `CREATE TABLE IF NOT EXISTS` y conserva los registros existentes. No subas bases de datos con información personal al repositorio.
