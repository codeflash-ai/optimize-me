"""
Custom OpenTelemetry auto-instrumentation for application functions.

This module provides automatic tracing of all functions in specified modules/packages
without requiring decorators. It works alongside opentelemetry-instrument for
library auto-instrumentation.

Usage:
    from src.telemetry.auto_instrumentation import auto_instrument_modules
    
    # Auto-instrument specific modules
    auto_instrument_modules(['src.numerical', 'src.algorithms', 'src.statistics'])
    
    # Or instrument all modules in a package
    auto_instrument_package('src')
"""
import functools
import importlib
import inspect
import logging
from typing import Any, Callable, List, Optional, Set

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

logger = logging.getLogger(__name__)

# Track already instrumented modules to avoid double instrumentation
_instrumented_modules: Set[str] = set()


def _get_tracer():
    """Get tracer dynamically to ensure it uses the current TracerProvider."""
    return trace.get_tracer(__name__)


def _wrap_function(func: Callable, module_name: str) -> Callable:
    """Wrap a function to automatically create spans for it."""
    func_name = func.__name__
    full_name = f"{module_name}.{func_name}"
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        tracer = _get_tracer()
        
        # Create span name from module and function name
        span_name = full_name
        
        with tracer.start_as_current_span(span_name) as span:
            try:
                # Add function metadata as span attributes
                span.set_attribute("code.function", func_name)
                span.set_attribute("code.namespace", module_name)
                
                # Optionally capture function signature info
                try:
                    sig = inspect.signature(func)
                    param_names = list(sig.parameters.keys())
                    span.set_attribute("code.function.parameters", ",".join(param_names))
                except Exception:
                    pass
                
                # Execute the function
                result = func(*args, **kwargs)
                
                span.set_status(Status(StatusCode.OK))
                return result
                
            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise
    
    return wrapper


def _instrument_module(module_name: str, include_private: bool = False) -> int:
    """
    Instrument all functions in a module.
    
    Args:
        module_name: Full module name (e.g., 'src.numerical.optimization')
        include_private: Whether to instrument private functions (starting with _)
    
    Returns:
        Number of functions instrumented
    """
    if module_name in _instrumented_modules:
        logger.debug(f"Module {module_name} already instrumented, skipping")
        return 0
    
    try:
        module = importlib.import_module(module_name)
        _instrumented_modules.add(module_name)
    except ImportError as e:
        logger.warning(f"Could not import module {module_name}: {e}")
        return 0
    
    instrumented_count = 0
    
    # Get all members of the module
    for name, obj in inspect.getmembers(module):
        # Only instrument callable objects that are functions
        if not inspect.isfunction(obj):
            continue
        
        # Skip private functions unless requested
        if not include_private and name.startswith('_'):
            continue
        
        # Skip if already wrapped (has our wrapper attribute)
        if hasattr(obj, '_otel_auto_instrumented'):
            continue
        
        # Skip if it's an imported function (not defined in this module)
        if obj.__module__ != module_name:
            continue
        
        try:
            # Wrap the function
            wrapped = _wrap_function(obj, module_name)
            wrapped._otel_auto_instrumented = True
            
            # Replace the function in the module
            setattr(module, name, wrapped)
            instrumented_count += 1
            
            logger.debug(f"Instrumented function: {module_name}.{name}")
        except Exception as e:
            logger.warning(f"Failed to instrument {module_name}.{name}: {e}")
    
    if instrumented_count > 0:
        logger.info(f"Instrumented {instrumented_count} functions in {module_name}")
    
    return instrumented_count


def auto_instrument_modules(
    module_names: List[str],
    include_private: bool = False,
    recursive: bool = False
) -> int:
    """
    Automatically instrument all functions in the specified modules.
    
    Args:
        module_names: List of module names to instrument (e.g., ['src.numerical.optimization'])
        include_private: Whether to instrument private functions (starting with _)
        recursive: If True, also instrument submodules
    
    Returns:
        Total number of functions instrumented
    
    Example:
        auto_instrument_modules(['src.numerical', 'src.algorithms'])
    """
    total_instrumented = 0
    
    for module_name in module_names:
        try:
            # Import the module first
            module = importlib.import_module(module_name)
            
            # Instrument the module itself
            count = _instrument_module(module_name, include_private)
            total_instrumented += count
            
            # If recursive, find and instrument submodules
            if recursive:
                import pkgutil
                if hasattr(module, '__path__'):
                    for finder, name, ispkg in pkgutil.walk_packages(module.__path__, module_name + '.'):
                        if not ispkg:  # Only instrument modules, not packages
                            submodule_name = name
                            count = _instrument_module(submodule_name, include_private)
                            total_instrumented += count
        except Exception as e:
            logger.warning(f"Failed to instrument module {module_name}: {e}")
    
    logger.info(f"Auto-instrumentation complete: {total_instrumented} functions instrumented")
    return total_instrumented


def auto_instrument_package(
    package_name: str,
    include_private: bool = False,
    exclude_modules: Optional[List[str]] = None
) -> int:
    """
    Automatically instrument all modules in a package.
    
    Args:
        package_name: Package name (e.g., 'src' or 'src.numerical')
        include_private: Whether to instrument private functions
        exclude_modules: List of module names to exclude from instrumentation
    
    Returns:
        Total number of functions instrumented
    
    Example:
        auto_instrument_package('src', exclude_modules=['src.tests'])
    """
    exclude_modules = exclude_modules or []
    total_instrumented = 0
    
    try:
        package = importlib.import_module(package_name)
    except ImportError as e:
        logger.error(f"Could not import package {package_name}: {e}")
        return 0
    
    if not hasattr(package, '__path__'):
        logger.warning(f"{package_name} is not a package")
        return 0
    
    import pkgutil
    
    # Walk through all modules in the package
    for finder, name, ispkg in pkgutil.walk_packages(package.__path__, package_name + '.'):
        # Skip excluded modules
        if any(excluded in name for excluded in exclude_modules):
            logger.debug(f"Skipping excluded module: {name}")
            continue
        
        # Skip packages, only instrument modules
        if ispkg:
            continue
        
        try:
            count = _instrument_module(name, include_private)
            total_instrumented += count
        except Exception as e:
            logger.warning(f"Failed to instrument module {name}: {e}")
    
    logger.info(f"Auto-instrumentation of package {package_name} complete: {total_instrumented} functions instrumented")
    return total_instrumented


def auto_instrument_current_package(
    include_private: bool = False,
    exclude_modules: Optional[List[str]] = None
) -> int:
    """
    Automatically instrument all modules in the current package (where this function is called).
    
    This is useful for instrumenting all modules in a package from within that package.
    
    Args:
        include_private: Whether to instrument private functions
        exclude_modules: List of module names to exclude
    
    Returns:
        Total number of functions instrumented
    """
    import sys
    
    # Get the calling module's package
    frame = inspect.currentframe()
    if frame is None or frame.f_back is None:
        logger.error("Could not determine current package")
        return 0
    
    calling_module = frame.f_back.f_globals.get('__name__', '')
    if not calling_module:
        logger.error("Could not determine calling module")
        return 0
    
    # Extract package name (everything except the last component)
    package_name = '.'.join(calling_module.split('.')[:-1])
    if not package_name:
        package_name = calling_module
    
    logger.info(f"Auto-instrumenting current package: {package_name}")
    return auto_instrument_package(package_name, include_private, exclude_modules)

