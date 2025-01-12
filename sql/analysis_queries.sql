-- 1) Customer lifetime value by segment (CTE + joins)
WITH customer_revenue AS (
    SELECT
        c.customer_id,
        c.segment,
        SUM(o.sales) AS lifetime_revenue
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.segment
)
SELECT
    segment,
    AVG(lifetime_revenue) AS avg_lifetime_revenue,
    MAX(lifetime_revenue) AS top_customer_value
FROM customer_revenue
GROUP BY segment
ORDER BY avg_lifetime_revenue DESC;

-- 2) Top 10 products by sales (subquery)
SELECT *
FROM (
    SELECT
        p.product_id,
        p.category,
        SUM(o.sales) AS product_sales
    FROM orders o
    JOIN products p ON p.product_id = o.product_id
    GROUP BY p.product_id, p.category
) t
ORDER BY product_sales DESC
LIMIT 10;

-- 3) Monthly sales and growth rate (CTE)
WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        SUM(sales) AS total_sales
    FROM orders
    GROUP BY 1
)
SELECT
    month,
    total_sales,
    (total_sales - LAG(total_sales) OVER (ORDER BY month))
        / NULLIF(LAG(total_sales) OVER (ORDER BY month), 0) AS growth_rate
FROM monthly_sales
ORDER BY month;
