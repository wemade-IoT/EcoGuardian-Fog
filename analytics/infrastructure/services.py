from analytics.domain.entities import Metric

class ExternalMetricServiceFacade:
    @staticmethod
    def get_metrics(self, metrics: list[Metric]) -> dict[int,int]:
        report = {}
        for metric in metrics:
            if metric.metric_types_id is not report:
                report[metric.metric_types_id] = 0
            if metric.metric_types_id in report:
                report[metric.metric_types_id] += metric.value
        return report






