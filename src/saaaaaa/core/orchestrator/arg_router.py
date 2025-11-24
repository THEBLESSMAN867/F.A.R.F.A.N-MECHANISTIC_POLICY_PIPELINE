"""
arg_router.py - Sistema de routing con auto-discovery de rutas especiales.

DISEÑO REFACTORIZADO:
- Decorador @special_route para marcar métodos con especificaciones de parámetros
- Auto-discovery: ExtendedArgRouter descubre rutas desde decoradores
- Sin hardcoding: Las rutas se mantienen junto al código que implementan
- Type-safe: Validación basada en type hints de Python
"""

from __future__ import annotations

import functools
import inspect
import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, ParamSpec, TypeVar, get_type_hints

import structlog

logger = structlog.get_logger(__name__)

P = ParamSpec('P')
R = TypeVar('R')


# ============================================================================
# DECORADOR PARA RUTAS ESPECIALES
# ============================================================================

@dataclass
class RouteSpec:
    """Especificación de ruta especial para un método."""
    required_args: list[str]
    optional_args: list[str]
    accepts_kwargs: bool
    description: str


def special_route(
    *,
    required: list[str],
    optional: list[str] = None,
    accepts_kwargs: bool = False,
    description: str = ""
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorador para marcar métodos con especificaciones de ruta especial.

    Uso:
        @special_route(required=['content'], optional=['context'], accepts_kwargs=True)
        def _extract_quantitative_claims(self, content: str, context: dict = None, **kwargs):
            ...

    Args:
        required: Lista de argumentos requeridos
        optional: Lista de argumentos opcionales
        accepts_kwargs: Si el método acepta **kwargs
        description: Descripción legible del método

    Returns:
        Decorador que añade __route_spec__ al método
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        route_spec = RouteSpec(
            required_args=required,
            optional_args=optional or [],
            accepts_kwargs=accepts_kwargs,
            description=description or func.__doc__ or ""
        )

        # Attach to function
        func.__route_spec__ = route_spec  # type: ignore[attr-defined]

        logger.debug(
            f"Registered special route: {func.__name__}",
            required=required,
            optional=optional or [],
            accepts_kwargs=accepts_kwargs
        )

        return func

    return decorator


# ============================================================================
# ARG ROUTER CON AUTO-DISCOVERY
# ============================================================================

class ExtendedArgRouter:
    """
    Router de argumentos con auto-discovery de rutas especiales.

    RESPONSABILIDADES:
    1. Validar que los argumentos pasados coincidan con la firma del método
    2. Convertir kwargs en args/kwargs apropiados para invocación
    3. Detectar automáticamente rutas especiales vía decoradores
    4. Prevenir silent drops de parámetros

    NO ES RESPONSABLE DE:
    - Cargar datos desde disco
    - Instanciar clases
    - Ejecutar lógica de negocio
    """

    def __init__(self, class_registry: dict[str, type]) -> None:
        """
        Inicializar router con registro de clases.

        Args:
            class_registry: Mapeo de nombre_clase -> tipo_clase
        """
        self._class_registry = dict(class_registry)
        self._special_routes = self._discover_special_routes()
        self._validation_cache: dict[tuple[str, str], Any] = {}

        logger.info(
            "ExtendedArgRouter initialized",
            classes=len(self._class_registry),
            special_routes=len(self._special_routes)
        )

    def _discover_special_routes(self) -> dict[str, RouteSpec]:
        """
        Auto-descubrir rutas especiales desde decoradores.

        Returns:
            dict mapping method_name -> RouteSpec
        """
        routes = {}

        for class_name, cls in self._class_registry.items():
            for method_name in dir(cls):
                # Skip private/magic methods
                if method_name.startswith('_') and not method_name.startswith('__'):
                    method = getattr(cls, method_name, None)

                    if callable(method) and hasattr(method, '__route_spec__'):
                        route_spec = method.__route_spec__

                        # Use fully qualified name to avoid collisions
                        full_name = f"{class_name}.{method_name}"
                        routes[full_name] = route_spec

                        logger.debug(
                            f"Discovered special route: {full_name}",
                            required=route_spec.required_args,
                            optional=route_spec.optional_args
                        )

        logger.info(f"Discovered {len(routes)} special routes via decorators")
        return routes

    def route(
        self,
        class_name: str,
        method_name: str,
        payload: dict[str, Any]
    ) -> tuple[tuple[Any, ...], dict[str, Any]]:
        """
        Validar y rutear argumentos para invocación de método.

        Args:
            class_name: Nombre de la clase
            method_name: Nombre del método
            payload: Argumentos como diccionario

        Returns:
            Tupla de (args, kwargs) para invocación

        Raises:
            ArgumentValidationError: Si validación falla
        """
        full_name = f"{class_name}.{method_name}"

        # Check if special route exists
        if full_name in self._special_routes:
            return self._route_special(full_name, payload)

        # Fallback to signature-based routing
        return self._route_by_signature(class_name, method_name, payload)

    def _route_special(
        self,
        full_name: str,
        payload: dict[str, Any]
    ) -> tuple[tuple[Any, ...], dict[str, Any]]:
        """Rutear usando especificación de ruta especial."""
        spec = self._special_routes[full_name]
        provided = set(payload.keys())
        required = set(spec.required_args)
        expected = required | set(spec.optional_args)

        # Validar argumentos requeridos
        missing = required - provided
        if missing:
            raise ArgumentValidationError(
                full_name.split('.')[0],
                full_name.split('.')[1],
                missing=missing
            )

        # Validar argumentos inesperados
        unexpected = provided - expected
        if unexpected and not spec.accepts_kwargs:
            raise ArgumentValidationError(
                full_name.split('.')[0],
                full_name.split('.')[1],
                unexpected=unexpected
            )

        # Todos los argumentos van a kwargs para rutas especiales
        return (), dict(payload)

    def _route_by_signature(
        self,
        class_name: str,
        method_name: str,
        payload: dict[str, Any]
    ) -> tuple[tuple[Any, ...], dict[str, Any]]:
        """Rutear basado en introspección de firma del método."""
        cls = self._class_registry.get(class_name)
        if not cls:
            raise ValueError(f"Class {class_name} not in registry")

        method = getattr(cls, method_name, None)
        if not method or not callable(method):
            raise ValueError(f"Method {method_name} not found in {class_name}")

        # Obtener firma
        sig = inspect.signature(method)
        params = sig.parameters

        # Separar parámetros requeridos y opcionales
        required = set()
        optional = set()
        has_var_keyword = False

        for param_name, param in params.items():
            if param_name == 'self':
                continue

            if param.kind == inspect.Parameter.VAR_KEYWORD:
                has_var_keyword = True
                continue

            if param.default is inspect.Parameter.empty:
                required.add(param_name)
            else:
                optional.add(param_name)

        provided = set(payload.keys())

        # Validar
        missing = required - provided
        if missing:
            raise ArgumentValidationError(
                class_name,
                method_name,
                missing=missing
            )

        unexpected = provided - (required | optional)
        if unexpected and not has_var_keyword:
            raise ArgumentValidationError(
                class_name,
                method_name,
                unexpected=unexpected
            )

        # Construir args y kwargs
        args = []
        kwargs = dict(payload)

        return tuple(args), kwargs


class ArgumentValidationError(ValueError):
    """Error de validación de argumentos."""

    def __init__(
        self,
        class_name: str,
        method_name: str,
        *,
        missing: set[str] = None,
        unexpected: set[str] = None
    ):
        self.class_name = class_name
        self.method_name = method_name
        self.missing = missing or set()
        self.unexpected = unexpected or set()

        parts = []
        if self.missing:
            parts.append(f"missing: {sorted(self.missing)}")
        if self.unexpected:
            parts.append(f"unexpected: {sorted(self.unexpected)}")

        message = f"Validation failed for {class_name}.{method_name}"
        if parts:
            message += f" ({', '.join(parts)})"

        super().__init__(message)


__all__ = [
    'special_route',
    'RouteSpec',
    'ExtendedArgRouter',
    'ArgumentValidationError',
]
