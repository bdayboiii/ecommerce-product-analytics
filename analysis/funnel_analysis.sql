-- 1. Overall funnel
SELECT
    event_type,
    COUNT(DISTINCT session_id) AS sessions
FROM events
GROUP BY event_type
ORDER BY
    CASE event_type
        WHEN 'view' THEN 1
        WHEN 'add_to_cart' THEN 2
        WHEN 'checkout' THEN 3
        WHEN 'purchase' THEN 4
    END;


-- 2. New vs Existing Users
WITH session_users AS (
    SELECT DISTINCT
        e.session_id,
        e.user_id,
        u.signup_date,
        MIN(e.event_timestamp::date) AS session_date
    FROM events e
    JOIN users u
        ON e.user_id = u.user_id
    GROUP BY
        e.session_id,
        e.user_id,
        u.signup_date
),

classified AS (
    SELECT
        *,
        CASE
            WHEN session_date - signup_date <= 30
            THEN 'New'
            ELSE 'Existing'
        END AS user_type
    FROM session_users
)

SELECT
    user_type,
    COUNT(*) AS sessions
FROM classified
GROUP BY user_type;


-- 3. New vs Existing × Price Segment
WITH session_data AS (
    SELECT
        e.session_id,
        e.user_id,
        e.product_id,

        MIN(e.event_timestamp::date) AS session_date,

        MAX(CASE
            WHEN e.event_type = 'view'
            THEN 1 ELSE 0
        END) AS viewed,

        MAX(CASE
            WHEN e.event_type = 'add_to_cart'
            THEN 1 ELSE 0
        END) AS added_to_cart

    FROM events e
    GROUP BY
        e.session_id,
        e.user_id,
        e.product_id
)

SELECT
    CASE
        WHEN sd.session_date - u.signup_date <= 30
        THEN 'New'
        ELSE 'Existing'
    END AS user_type,

    CASE
        WHEN p.price < 2000 THEN 'Low (<2000)'
        WHEN p.price < 4000 THEN 'Medium (2000-3999)'
        ELSE 'High (4000+)'
    END AS price_segment,

    COUNT(*) AS viewed_sessions,

    SUM(sd.added_to_cart) AS cart_sessions,

    ROUND(
        100.0 * SUM(sd.added_to_cart) / COUNT(*),
        2
    ) AS view_to_cart_pct

FROM session_data sd

JOIN users u
    ON sd.user_id = u.user_id

JOIN products p
    ON sd.product_id = p.product_id

WHERE sd.viewed = 1

GROUP BY
    user_type,
    price_segment

ORDER BY
    user_type,
    price_segment;