"""Interfaz Gradio de la miniaplicación.

Uso:
    python app.py            abre la interfaz en el navegador
    python app.py --probar   consulta los sensores de prueba y guarda las respuestas en Markdown
"""
import argparse
import logging
from datetime import date
from pathlib import Path

import gradio as gr
from langchain_core.language_models import BaseChatModel

from logica import crear_modelo, responder

SENSORES_DE_PRUEBA = ["temperatura de celda", "presión", "caudal de H₂"]


def crear_interfaz(modelo: BaseChatModel) -> gr.Interface:
    def al_enviar(sensor: str) -> str:
        return responder(sensor, modelo)

    return gr.Interface(
        fn=al_enviar,
        inputs=[gr.Textbox(label="Sensor", lines=1)],
        outputs=[gr.Markdown()],
        flagging_mode="never",
        title="Analizador de sensores de electrolizador",
        description="Introduce el nombre de un sensor y obtén su análisis operativo",
    )


def probar_sensores(modelo: BaseChatModel, destino: Path) -> None:
    bloques = [f"## {sensor}\n\n{responder(sensor, modelo)}\n" for sensor in SENSORES_DE_PRUEBA]
    destino.write_text(f"# Pruebas {date.today()}\n\n" + "\n".join(bloques), encoding="utf-8")
    print(f"Respuestas guardadas en {destino}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--probar", action="store_true", help="consulta los sensores de prueba sin abrir la interfaz")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    modelo = crear_modelo()

    if args.probar:
        probar_sensores(modelo, Path(__file__).with_name(f"pruebas-{date.today()}.md"))
    else:
        crear_interfaz(modelo).launch()


if __name__ == "__main__":
    main()
