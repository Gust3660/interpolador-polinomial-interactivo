# Interpolador polinomial interactivo

Aplicación Streamlit para definir puntos y construir el polinomio que pasa por todos ellos con los métodos de Lagrange o Newton.

## Funciones

- Edita, agrega o elimina pares de nodos `(x, y)`.
- Selecciona el método de interpolación.
- Grafica el polinomio y calcula su valor en un punto elegido.
- Valida que los nodos sean finitos y que no se repitan los valores `x`.

## Estructura

```text
.
├── backend.py       # Validación y algoritmos de interpolación
├── frontend.py      # Interfaz y gráfica
├── requirements.txt
└── README.md
```

## Instalación y ejecución

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run frontend.py
```

En macOS o Linux, activa el entorno con `source .venv/bin/activate`.

El polinomio pasa exactamente por los nodos, pero agregar muchos puntos puede generar oscilaciones entre ellos, especialmente en los extremos.
