"""SourceConnector for global-health-data-pipeline v2.

Core module implementing source_connector functionality for the
global health data pipeline system.
"""
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class SourceConnectorConfig:
    """Configuration for source_connector."""
    enabled: bool = True
    batch_size: int = 200
    timeout: int = 20
    max_retries: int = 3


@dataclass
class SourceConnectorResult:
    """Result from source_connector execution."""
    success: bool
    data: List[Dict[str, Any]] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    duration_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class SourceConnector:
    """Primary source_connector handler for global-health-data-pipeline.

    Provides core source connector capabilities including
    batch processing, validation, and result aggregation.
    """

    def __init__(self, config: Optional[SourceConnectorConfig] = None):
        self.config = config or SourceConnectorConfig()
        self._initialized = False
        self._run_count = 0
        self._start_time = datetime.utcnow()

    def initialize(self) -> None:
        if self._initialized:
            return
        logger.info("Initializing source_connector for global-health-data-pipeline")
        self._initialized = True

    def execute(self, inputs: List[Dict[str, Any]]) -> SourceConnectorResult:
        self.initialize()
        self._run_count += 1
        start = datetime.utcnow()

        results = []
        errors = []

        for batch_start in range(0, len(inputs), self.config.batch_size):
            batch = inputs[batch_start:batch_start + self.config.batch_size]
            for item in batch:
                try:
                    processed = self._process_item(item)
                    if self._validate(processed):
                        results.append(processed)
                except Exception as e:
                    errors.append(f"Item {item.get('id', '?')}: {e}")

        duration = (datetime.utcnow() - start).total_seconds() * 1000

        return SourceConnectorResult(
            success=len(errors) == 0,
            data=results,
            errors=errors,
            duration_ms=duration,
            metadata={
                "run": self._run_count,
                "input_count": len(inputs),
                "output_count": len(results),
                "error_count": len(errors),
            },
        )

    def _process_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            **item,
            "processed_by": "source_connector",
            "version": 2,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _validate(self, item: Dict[str, Any]) -> bool:
        return bool(item.get("id")) or bool(item.get("processed_by"))

    @property
    def metrics(self) -> Dict[str, Any]:
        uptime = (datetime.utcnow() - self._start_time).total_seconds()
        return {
            "runs": self._run_count,
            "uptime_s": uptime,
            "initialized": self._initialized,
        }
