from analytics.infrastructure.services import ExternalMetricServiceFacade


class MetricService:
    def __init__(self, external_metric_service: ExternalMetricServiceFacade):
        self.external_metric_service = external_metric_service

    def get_average_consume(self, metrics: list) -> dict[int, int]:
        return self.external_metric_service.get_metrics(metrics)