-- 1) Monthly profitability with window functions
SELECT
    DATE_TRUNC('month', order_ts) AS month,
    SUM(net_sales) AS net_sales,
    SUM(profit) AS total_profit,
    SUM(profit) / NULLIF(SUM(net_sales), 0) AS profit_margin,
    SUM(net_sales) - LAG(SUM(net_sales)) OVER (ORDER BY DATE_TRUNC('month', order_ts)) AS mom_net_sales_delta
FROM orders
GROUP BY 1
ORDER BY 1;

-- 2) Cohort retention (CTE)
WITH base AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', order_ts) AS order_month,
        MIN(DATE_TRUNC('month', order_ts)) OVER (PARTITION BY customer_id) AS cohort_month
    FROM orders
    WHERE order_status = 'completed'
),
cohort_counts AS (
    SELECT
        cohort_month,
        EXTRACT(MONTH FROM AGE(order_month, cohort_month)) +
        12 * EXTRACT(YEAR FROM AGE(order_month, cohort_month)) AS cohort_index,
        COUNT(DISTINCT customer_id) AS active_customers
    FROM base
    GROUP BY 1, 2
),
cohort_size AS (
    SELECT cohort_month, active_customers AS cohort_size
    FROM cohort_counts
    WHERE cohort_index = 0
)
SELECT
    c.cohort_month,
    c.cohort_index,
    c.active_customers,
    s.cohort_size,
    c.active_customers::NUMERIC / NULLIF(s.cohort_size, 0) AS retention_rate
FROM cohort_counts c
JOIN cohort_size s USING (cohort_month)
ORDER BY 1, 2;

-- 3) Campaign and channel efficiency
SELECT
    channel,
    campaign,
    COUNT(DISTINCT order_id) AS orders,
    SUM(net_sales) AS net_sales,
    SUM(profit) AS profit,
    SUM(profit) / NULLIF(SUM(net_sales), 0) AS margin
FROM orders
GROUP BY channel, campaign
ORDER BY net_sales DESC;

-- 4) Top customers by CLV proxy
SELECT
    customer_id,
    SUM(net_sales) AS lifetime_value,
    COUNT(DISTINCT order_id) AS order_count,
    AVG(net_sales) AS avg_order_value
FROM orders
WHERE order_status = 'completed'
GROUP BY customer_id
ORDER BY lifetime_value DESC
LIMIT 50;
