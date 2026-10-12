
-- =========================================================
-- CUSTOMER SHOPPING BEHAVIOR: ADVANCED SQL ANALYTICS
-- Database: SQLite
-- =========================================================


-- 1. Overall business KPIs
SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT "Customer ID") AS unique_customers,
    ROUND(AVG("Purchase Amount (USD)"), 2) AS avg_purchase_amount,
    ROUND(AVG("Review Rating"), 2) AS avg_review_rating,
    SUM("Purchase Amount (USD)") AS total_purchase_amount,
    SUM(CASE
        WHEN "Subscription Status" = 'Yes' THEN 1
        ELSE 0
    END) AS subscribed_records
FROM customer_shopping_behavior;


-- 2. Revenue and customer count by product category
SELECT
    Category,
    COUNT(*) AS customer_records,
    SUM("Purchase Amount (USD)") AS total_purchase_amount,
    ROUND(AVG("Purchase Amount (USD)"), 2) AS avg_purchase_amount
FROM customer_shopping_behavior
GROUP BY Category
ORDER BY total_purchase_amount DESC;


-- 3. Purchasing behavior by subscription status
SELECT
    "Subscription Status" AS subscription_status,
    COUNT(*) AS customer_records,
    ROUND(AVG("Purchase Amount (USD)"), 2) AS avg_purchase_amount,
    ROUND(AVG("Previous Purchases"), 2) AS avg_previous_purchases,
    ROUND(AVG("Review Rating"), 2) AS avg_review_rating
FROM customer_shopping_behavior
GROUP BY "Subscription Status"
ORDER BY avg_purchase_amount DESC;


-- 4. Discount usage analysis
SELECT
    "Discount Applied" AS discount_applied,
    COUNT(*) AS customer_records,
    ROUND(AVG("Purchase Amount (USD)"), 2) AS avg_purchase_amount,
    SUM("Purchase Amount (USD)") AS total_purchase_amount
FROM customer_shopping_behavior
GROUP BY "Discount Applied"
ORDER BY avg_purchase_amount DESC;


-- 5. Promo code usage analysis
SELECT
    "Promo Code Used" AS promo_code_used,
    COUNT(*) AS customer_records,
    ROUND(AVG("Purchase Amount (USD)"), 2) AS avg_purchase_amount,
    ROUND(AVG("Review Rating"), 2) AS avg_review_rating
FROM customer_shopping_behavior
GROUP BY "Promo Code Used";


-- 6. Purchase behavior by reported frequency
SELECT
    "Frequency of Purchases" AS purchase_frequency,
    COUNT(*) AS customer_records,
    ROUND(AVG("Purchase Amount (USD)"), 2) AS avg_purchase_amount,
    ROUND(AVG("Previous Purchases"), 2) AS avg_previous_purchases
FROM customer_shopping_behavior
GROUP BY "Frequency of Purchases"
ORDER BY avg_previous_purchases DESC;


-- 7. Product category performance by season
SELECT
    Season,
    Category,
    COUNT(*) AS customer_records,
    SUM("Purchase Amount (USD)") AS total_purchase_amount,
    ROUND(AVG("Purchase Amount (USD)"), 2) AS avg_purchase_amount
FROM customer_shopping_behavior
GROUP BY Season, Category
ORDER BY Season, total_purchase_amount DESC;


-- 8. Customer spending groups
SELECT
    CASE
        WHEN "Purchase Amount (USD)" >= 75 THEN 'High Purchase Amount'
        WHEN "Purchase Amount (USD)" >= 50 THEN 'Medium Purchase Amount'
        ELSE 'Lower Purchase Amount'
    END AS spending_group,
    COUNT(*) AS customer_records,
    ROUND(AVG("Purchase Amount (USD)"), 2) AS avg_purchase_amount,
    ROUND(AVG("Previous Purchases"), 2) AS avg_previous_purchases
FROM customer_shopping_behavior
GROUP BY spending_group
ORDER BY avg_purchase_amount DESC;


-- 9. Review ratings by product category
SELECT
    Category,
    COUNT("Review Rating") AS ratings_available,
    ROUND(AVG("Review Rating"), 2) AS avg_review_rating,
    MIN("Review Rating") AS minimum_rating,
    MAX("Review Rating") AS maximum_rating
FROM customer_shopping_behavior
GROUP BY Category
ORDER BY avg_review_rating DESC;


-- 10. Payment method analysis
SELECT
    "Payment Method" AS payment_method,
    COUNT(*) AS customer_records,
    ROUND(AVG("Purchase Amount (USD)"), 2) AS avg_purchase_amount,
    SUM("Purchase Amount (USD)") AS total_purchase_amount
FROM customer_shopping_behavior
GROUP BY "Payment Method"
ORDER BY total_purchase_amount DESC;
