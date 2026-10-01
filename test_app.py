"""Tests de presentación de la interfaz; no llaman a la API."""
import gradio as gr
from langchain_core.language_models.fake_chat_models import FakeListChatModel

from app import crear_interfaz


def test_salida_renderiza_markdown():
    modelo = FakeListChatModel(responses=["**Respuesta**"])
    interfaz = crear_interfaz(modelo)
    assert isinstance(interfaz.output_components[0], gr.Markdown)
