# Analizador LLM de sensores en electrolizadores

Miniaplicación académica que recibe el nombre de un sensor industrial y genera una explicación breve sobre qué mide, su importancia operativa y posibles anomalías. El proyecto utiliza **LangChain**, **Gemini 3.5 Flash-Lite** y una interfaz **Gradio**.

## Trabajo realizado

- Separación entre interfaz (`app.py`) y lógica (`logica.py`).
- Validación de entradas y manejo básico de errores de API.
- Gestión segura de la clave mediante `.env`.
- Doce tests unitarios sin llamadas reales a la API.
- Prueba con temperatura de celda, presión y caudal de H₂.
- Presentación de la respuesta con Markdown y prompt que evita diagnósticos categóricos.

## Ejecución

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
# Añadir GOOGLE_API_KEY al archivo .env
.\.venv\Scripts\python.exe app.py
```

Tests y prueba automática:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe app.py --probar
```

## Observación y limitación

El modelo relacionó un caudal elevado de H₂ con fugas internas de forma demasiado categórica. El caudal por sí solo no permite ese diagnóstico y, a corriente constante, un mayor crossover tendería a reducir el H₂ recuperable. También confundió temperatura con calor y exageró la capacidad del sensor de presión para garantizar pureza. El prompt revisado reduce afirmaciones absolutas, pero la verificación todavía exige documentación o datos reales.

Como trabajo posterior, PEACE permite comparar el caudal medido con la producción teórica obtenida mediante la ley de Faraday porque contiene corriente total y caudal de H₂. Esta comparación requerirá validar unidades, condiciones normales, pureza y número de celdas.

La [salida original y su revisión](resultados/pruebas-gemini-2026-10-01.md) se conservan sin alterar. La [prueba del prompt revisado](resultados/pruebas-prompt-revisado-2026-10-01.md) muestra que mejoró el lenguaje de incertidumbre y la separación entre medición y control, pero no eliminó el error técnico sobre crossover. Un prompt puede mitigar una limitación; no sustituye la evidencia.

## Referencias

- [Dataset PEACE (Zenodo)](https://doi.org/10.5281/zenodo.19605474).
- [Electrolysis Production (NREL)](https://www.hydrogen.energy.gov/docs/hydrogenprogramlibraries/pdfs/46676.pdf).
- [Componente Markdown de Gradio](https://www.gradio.app/main/docs/gradio/markdown).
