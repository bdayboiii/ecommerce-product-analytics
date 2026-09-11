-- 1. Compare control and treatment groups

SELECT
    experiment_group,

    COUNT(DISTINCT session_id) AS sessions,

    COUNT(DISTINCT CASE
        WHEN event_type = 'add_to_cart'
        THEN session_id
    END) AS cart_sessions,

    ROUND(
        100.0 *
        COUNT(DISTINCT CASE
            WHEN event_type = 'add_to_cart'
            THEN session_id
        END)
        / COUNT(DISTINCT session_id),
        2
    ) AS conversion_rate

FROM events

WHERE experiment_group IS NOT NULL

GROUP BY experiment_group

ORDER BY experiment_group;


-- 2. Calculate conversion lift

WITH experiment_results AS (

    SELECT
        experiment_group,

        COUNT(DISTINCT session_id) AS sessions,

        COUNT(DISTINCT CASE
            WHEN event_type = 'add_to_cart'
            THEN session_id
        END) AS cart_sessions

    FROM events

    WHERE experiment_group IS NOT NULL

    GROUP BY experiment_group
),

conversion_rates AS (

    SELECT
        MAX(
            CASE
                WHEN experiment_group = 'control'
                THEN cart_sessions * 1.0 / sessions
            END
        ) AS control_rate,

        MAX(
            CASE
                WHEN experiment_group = 'treatment'
                THEN cart_sessions * 1.0 / sessions
            END
        ) AS treatment_rate

    FROM experiment_results
)

SELECT

    ROUND(100.0 * control_rate, 2)
        AS control_conversion_pct,

    ROUND(100.0 * treatment_rate, 2)
        AS treatment_conversion_pct,

    ROUND(
        100.0 * (treatment_rate - control_rate),
        2
    )
        AS absolute_lift_percentage_points,

    ROUND(
        100.0 * (treatment_rate - control_rate)
        / control_rate,
        2
    )
        AS relative_lift_pct

FROM conversion_rates;


    -- 3. Check experiment group sizes

SELECT
    experiment_group,
    COUNT(DISTINCT session_id) AS sessions
FROM events
WHERE experiment_group IS NOT NULL
GROUP BY experiment_group
ORDER BY experiment_group;