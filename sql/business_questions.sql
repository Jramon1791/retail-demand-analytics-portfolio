-- 1) Monthly net revenue by region
SELECT
  month,
  region,
  SUM(net_after_returns) AS net_after_returns
FROM monthly_region_kpis
GROUP BY 1, 2
ORDER BY 1, 3 DESC;

-- 2) Top 10 customers by lifetime net revenue
SELECT
  customer_id,
  orders,
  lifetime_net_revenue
FROM customer_ltv
ORDER BY lifetime_net_revenue DESC
LIMIT 10;

-- 3) Products with high return risk and high revenue
SELECT
  category,
  product_name,
  net_revenue,
  return_rate
FROM product_performance
WHERE return_rate >= 0.08
ORDER BY net_revenue DESC;
