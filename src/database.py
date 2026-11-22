import sqlite3
from datetime import datetime
from pathlib import Path


DEFAULT_DB = Path(__file__).resolve().parent.parent / "finanzas.db"


def crear_tabla_transacciones(db=DEFAULT_DB):
    """Create the table if needed without deleting existing transactions."""
    with sqlite3.connect(str(db)) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transacciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                tipo TEXT NOT NULL CHECK(tipo IN ('ingreso', 'gasto')),
                monto REAL NOT NULL CHECK(monto > 0),
                descripcion TEXT NOT NULL
            )
            """
        )


def insertar_transaccion(tipo, descripcion, monto, db=DEFAULT_DB):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(str(db)) as conn:
        cursor = conn.execute(
            """
            INSERT INTO transacciones (fecha, tipo, monto, descripcion)
            VALUES (?, ?, ?, ?)
            """,
            (fecha, tipo, monto, descripcion),
        )
        return cursor.lastrowid


def obtener_transacciones(db=DEFAULT_DB):
    with sqlite3.connect(str(db)) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, fecha, tipo, monto, descripcion "
            "FROM transacciones ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]
