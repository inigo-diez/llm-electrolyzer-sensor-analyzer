"""Tests de la lógica. No llaman a la API: usan modelos falsos."""
import pytest
from langchain_core.language_models.fake_chat_models import FakeListChatModel

import logica
from logica import (
    MENSAJE_ERROR_API,
    EntradaInvalida,
    analizar_sensor,
    construir_prompt,
    crear_modelo,
    responder,
    validar_sensor,
)


class ModeloQueFalla:
    """Simula un proveedor caído."""

    def invoke(self, prompt):
        raise TimeoutError("el proveedor no responde")


def test_validar_quita_espacios():
    assert validar_sensor("  presión  ") == "presión"


@pytest.mark.parametrize("entrada", ["", "   ", None])
def test_validar_rechaza_vacio(entrada):
    with pytest.raises(EntradaInvalida):
        validar_sensor(entrada)


def test_validar_rechaza_entrada_larga():
    with pytest.raises(EntradaInvalida):
        validar_sensor("x" * 101)


def test_prompt_incluye_el_sensor():
    assert "caudal de H₂" in construir_prompt("caudal de H₂")


def test_prompt_exige_incertidumbre_diagnostica():
    prompt = construir_prompt("presión")
    assert "causas posibles" in prompt
    assert "no como diagnósticos confirmados" in prompt
    assert "el sensor mide, pero no regula" in prompt


def test_analizar_devuelve_texto_del_modelo():
    modelo = FakeListChatModel(responses=["Mide la temperatura del stack."])
    assert analizar_sensor("temperatura de celda", modelo) == "Mide la temperatura del stack."


def test_entrada_vacia_no_llega_al_modelo():
    assert responder("   ", ModeloQueFalla()) == "Introduce el nombre de un sensor."


def test_error_de_api_devuelve_mensaje_amable():
    assert responder("presión", ModeloQueFalla()) == MENSAJE_ERROR_API


def test_crear_modelo_sin_clave_falla_pronto(monkeypatch):
    monkeypatch.setattr(logica, "load_dotenv", lambda: None)
    monkeypatch.delenv(logica.VARIABLE_CLAVE, raising=False)
    with pytest.raises(RuntimeError, match=logica.VARIABLE_CLAVE):
        crear_modelo()
