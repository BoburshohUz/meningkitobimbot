# Sample Grafana Alerts

## 1. API Latency High (95 percentile > 1s)
histogram_quantile(0.95, sum by(le,endpoint) (http_request_latency_seconds_bucket{service="$service"}[2m])) > 1

## 2. High Request Volume (>300 req/min)
sum(rate(http_requests_total{service="$service"}[1m])) * 60 > 300

## 3. Chat Rate Limit Spike (>10 blocks /2m)
increase(chat_limit_exceeded_total{service="$service"}[2m]) > 10
