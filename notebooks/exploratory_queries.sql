-- 1. Total companies
SELECT COUNT(*) AS total_companies
FROM companies;

-- 2. Top 10 companies by ROE
SELECT company_name, roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

-- 3. Companies by sector
SELECT broad_sector, COUNT(*) AS total
FROM sectors
GROUP BY broad_sector;

-- 4. Top 10 companies by Market Cap
SELECT company_id, market_cap_crore
FROM market_cap
ORDER BY market_cap_crore DESC
LIMIT 10;

-- 5. Total stock price records
SELECT COUNT(*)
FROM stock_prices;

-- 6. Average Closing Price
SELECT AVG(close_price)
FROM stock_prices;

-- 7. Highest Net Profit
SELECT company_id, MAX(net_profit)
FROM profitandloss;

-- 8. Highest Sales
SELECT company_id, MAX(sales)
FROM profitandloss;

-- 9. Average Debt to Equity
SELECT AVG(debt_to_equity)
FROM financial_ratios;

-- 10. Total Companies in Peer Groups
SELECT COUNT(DISTINCT company_id)
FROM peer_groups;