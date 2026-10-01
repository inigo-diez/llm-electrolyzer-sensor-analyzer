"""Lógica de la miniaplicación: valida la entrada, construye el prompt y llama al modelo.

No depende de la interfaz, así que se puede probar sin Gradio y sin llamar a la API.
"""
import logging
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import PromptTemplate

MODELO = "gemini-3.5-flash-lite"
PROVEEDOR = "google_genai"
VARIABLE_CLAVE = "GOOGLE_API_KEY"

MAX_CARACTERES = 100
MENSAJE_ERROR_API = "No se pudo obtener respuesta del modelo. Inténtalo de nuevo en unos segundos."

PLANTILLA = PromptTemplate.from_template(
    "Explica el sensor {sensor} en un electrolizador de hidrógeno.\n"
    "Indica qué mide, su importancia operativa y las anomalías que podría señalar.\n"
    "Distingue medición y control: el sensor mide, pero no regula, mantiene ni garantiza el proceso.\n"
    "Presenta las anomalías como causas posibles, no como diagnósticos confirmados.\n"
    "No atribuyas una señal a una única causa sin datos adicionales y aclara si depende del tipo de electrolizador.\n"
    "Usa Markdown sencillo.\n"
    "Responde en menos de 100 palabras."
)

logger = logging.getLogger(__name__)


class EntradaInvalida(ValueError):
    """La entrada del usuario no es válida y no debe llegar a la API."""


def validar_sensor(sensor: str | None) -> str:
    sensor = (sensor or "").strip()
    if not sensor:
        raise EntradaInvalida("Introduce el nombre de un sensor.")
    if len(sensor) > MAX_CARACTERES:
        raise EntradaInvalida(f"El nombre del sensor no puede superar {MAX_CARACTERES} caracteres.")
    return sensor


def construir_prompt(sensor: str) -> str:
    return PLANTILLA.format(sensor=sensor)


def crear_modelo() -> BaseChatModel:
    """Lee la clave del entorno o de .env y falla pronto si no está."""
    load_dotenv()
    if not os.getenv(VARIABLE_CLAVE):
        raise RuntimeError(f"Falta {VARIABLE_CLAVE}. Defínela en un archivo .env (ver .env.example).")
    return init_chat_model(MODELO, model_provider=PROVEEDOR, max_tokens=300, timeout=60, max_retries=2)


def analizar_sensor(sensor: str, modelo: BaseChatModel) -> str:
    prompt = construir_prompt(validar_sensor(sensor))
    return modelo.invoke(prompt).text


def responder(sensor: str, modelo: BaseChatModel) -> str:
    """Devuelve siempre un texto apto para el usuario; el detalle técnico va al log."""
    try:
        return analizar_sensor(sensor, modelo)
    except EntradaInvalida as error:
        return str(error)
    except Exception:
        logger.exception("Fallo al consultar el modelo")
        return MENSAJE_ERROR_API
