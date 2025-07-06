from analytics.domain.entities import Metric

class ExternalMetricServiceFacade:
    @staticmethod
    def get_metrics(metrics: list[Metric]) -> dict[int, int]:
        consumption_metrics = [m.metric_value for m in metrics if m.metric_types_id == 4]
        if not consumption_metrics:
            return {4: 0}
        average = sum(consumption_metrics) / len(consumption_metrics)
        return {4: average}
