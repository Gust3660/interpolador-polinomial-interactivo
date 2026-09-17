"""Interfaz Streamlit para interpolación polinomial."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from backend import interpolate


st.set_page_config(page_title="Interpolador polinomial", page_icon="〰️", layout="wide")
st.title("Interpolador polinomial interactivo")
st.write("Define puntos y compara los polinomios de interpolación de Lagrange y Newton.")

default_nodes = pd.DataFrame({"x": [-2.0, -1.0, 0.0, 1.0, 2.0], "y": [4.0, 1.0, 0.0, 1.0, 4.0]})
nodes = st.data_editor(default_nodes, num_rows="dynamic", hide_index=True, use_container_width=True)
with st.sidebar:
    method = st.selectbox("Método", ["Newton", "Lagrange"])
try:
    clean_nodes = nodes.dropna()
    x_nodes, y_nodes = clean_nodes["x"].to_numpy(), clean_nodes["y"].to_numpy()
    if len(x_nodes) < 2:
        raise ValueError("Agrega al menos dos pares x,y.")
    if len(set(x_nodes)) != len(x_nodes):
        raise ValueError("Los valores x deben ser distintos.")
    padding = max(float(np.ptp(x_nodes)) * 0.15, 0.5)
    x_grid = np.linspace(float(min(x_nodes)) - padding, float(max(x_nodes)) + padding, 600)
    y_grid = interpolate(x_nodes, y_nodes, x_grid, method)
except (ValueError, KeyError) as error:
    st.error(str(error))
    st.stop()

evaluation_x = st.number_input(
    "Evaluar el polinomio en x =", min_value=float(min(x_nodes)),
    max_value=float(max(x_nodes)), value=float(np.mean(x_nodes)), step=0.1,
)
evaluation_y = float(interpolate(x_nodes, y_nodes, np.array([evaluation_x]), method)[0])
st.metric(f"P({evaluation_x:g})", f"{evaluation_y:.8g}")

fig, axis = plt.subplots(figsize=(10, 5))
axis.plot(x_grid, y_grid, label=f"Interpolante ({method})")
axis.scatter(x_nodes, y_nodes, color="tab:red", label="Nodos", zorder=3)
axis.scatter([evaluation_x], [evaluation_y], color="black", marker="x", label="Evaluación", zorder=4)
axis.set(title="Polinomio interpolante", xlabel="x", ylabel="P(x)")
axis.grid(True, alpha=0.3)
axis.legend()
fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)
st.caption("Con muchos nodos equidistantes, el polinomio puede oscilar entre los puntos (fenómeno de Runge).")
