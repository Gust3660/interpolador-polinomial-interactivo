"""Interpolación polinomial de Lagrange y Newton."""

from __future__ import annotations

import numpy as np


def _validate_nodes(x_nodes, y_nodes) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray(x_nodes, dtype=float)
    y = np.asarray(y_nodes, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size or x.size < 2:
        raise ValueError("Se necesitan al menos dos pares de nodos x,y.")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
        raise ValueError("Todos los nodos deben ser valores finitos.")
    if np.unique(x).size != x.size:
        raise ValueError("Los valores x de los nodos deben ser distintos.")
    return x, y


def interpolate(x_nodes, y_nodes, x_values, method: str = "Newton") -> np.ndarray:
    x, y = _validate_nodes(x_nodes, y_nodes)
    points = np.asarray(x_values, dtype=float)
    if method == "Lagrange":
        output = np.zeros_like(points, dtype=float)
        for i in range(x.size):
            basis = np.ones_like(points, dtype=float)
            for j in range(x.size):
                if i != j:
                    basis *= (points - x[j]) / (x[i] - x[j])
            output += y[i] * basis
        return output
    if method == "Newton":
        coefficients = y.copy()
        for order in range(1, x.size):
            coefficients[order:] = (coefficients[order:] - coefficients[order - 1:-1]) / (x[order:] - x[:-order])
        output = np.full_like(points, coefficients[-1], dtype=float)
        for index in range(x.size - 2, -1, -1):
            output = coefficients[index] + (points - x[index]) * output
        return output
    raise ValueError("El método debe ser Lagrange o Newton.")
