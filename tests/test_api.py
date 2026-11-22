import pytest
from fastapi.testclient import TestClient

import main
from src.transacciones import GestorFinanzas


@pytest.fixture
def client(tmp_path, monkeypatch):
    database = tmp_path / "test_finanzas.db"
    monkeypatch.setattr(main, "gestor", GestorFinanzas(db=database))
    return TestClient(main.app)


def test_root_and_docs(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"
    assert client.get("/docs").status_code == 200


def test_register_income_and_expense_and_balance(client):
    income = client.post(
        "/transacciones/ingreso",
        json={"descripcion": "Salario", "monto": 1000},
    )
    expense = client.post(
        "/transacciones/gasto",
        json={"descripcion": "Comida", "monto": 250},
    )

    assert income.status_code == 201
    assert expense.status_code == 201
    assert client.get("/balance/").json()["balance"] == 750


def test_list_transactions(client):
    client.post(
        "/transacciones/ingreso",
        json={"descripcion": "Salario", "monto": 500},
    )
    response = client.get("/transacciones/")

    assert response.status_code == 200
    assert len(response.json()["transacciones"]) == 1
    assert response.json()["transacciones"][0]["descripcion"] == "Salario"


def test_reject_expense_without_funds(client):
    response = client.post(
        "/transacciones/gasto",
        json={"descripcion": "Renta", "monto": 100},
    )
    assert response.status_code == 409


@pytest.mark.parametrize("payload", [
    {"descripcion": "Salario", "monto": 0},
    {"descripcion": "Salario", "monto": -10},
    {"descripcion": "   ", "monto": 10},
])
def test_reject_invalid_transaction(client, payload):
    response = client.post("/transacciones/ingreso", json=payload)
    assert response.status_code == 422


def test_database_initialization_preserves_existing_data(tmp_path):
    database = tmp_path / "persistencia.db"
    gestor_temp = GestorFinanzas(db=database)
    gestor_temp.agregar_ingreso(200, "Ahorros")

    gestor_again = GestorFinanzas(db=database)
    assert len(gestor_again.obtener_transacciones()) == 1
