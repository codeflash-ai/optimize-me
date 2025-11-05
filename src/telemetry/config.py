import os
from typing import Optional


class TelemetryConfig:
    enabled: bool = os.getenv("OTEL_SDK_DISABLED", "false").lower() != "true"
    service_name: str = os.getenv("OTEL_SERVICE_NAME", "optimize-me")
    service_version: str = os.getenv("OTEL_SERVICE_VERSION", "0.1.0")
    exporter_type: str = os.getenv("OTEL_EXPORTER_TYPE", "console")
    exporter_endpoint: str = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318")
    sampling_rate: float = float(os.getenv("OTEL_TRACES_SAMPLER_ARG", "1.0"))
    log_level: str = os.getenv("OTEL_LOG_LEVEL", "INFO")

    @classmethod
    def get_exporter_config(cls) -> dict:
        config = {"type": cls.exporter_type}
        if cls.exporter_type in ["otlp", "jaeger"]:
            config["endpoint"] = cls.exporter_endpoint
        return config

