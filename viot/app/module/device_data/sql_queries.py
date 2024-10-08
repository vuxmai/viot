FROM_WHERE_CLAUSE: str = """
    FROM device_data
    WHERE device_data.device_id = :device_id
    AND device_data.key = :key
    AND device_data.ts >= :start_date AND device_data.ts <= :end_date
    GROUP BY device_data.key, bucket
    ORDER BY device_data.key, bucket
"""

FIND_AVG_QUERY: str = """
    SELECT
    time_bucket(:bucket_width, device_data.ts, :timezone, :start_date) AS bucket,
    :bucket_width AS interval,
    SUM(COALESCE(device_data.long_v, 0)) AS long_value,
    SUM(COALESCE(device_data.double_v, 0)) AS double_value,
    SUM(CASE WHEN device_data.long_v IS NULL THEN 0 ELSE 1 END) AS count_long_value,
    SUM(CASE WHEN device_data.double_v IS NULL THEN 0 ELSE 1 END) AS count_double_value,
    MAX(device_data.ts) AS agg_values_last_ts
"""

FIND_MAX_QUERY: str = """
    SELECT
    time_bucket(:bucket_width, device_data.ts, :timezone, :start_date) AS bucket,
    :bucket_width AS interval,
    MAX(COALESCE(device_data.long_v, -9223372036854775807)) AS long_value,
    MAX(COALESCE(device_data.double_v, -1.79769E+308)) AS double_value,
    MAX(device_data.ts) AS agg_values_last_ts
"""

FIND_MIN_QUERY: str = """
    SELECT
    time_bucket(:bucket_width, device_data.ts, :timezone, :start_date) AS bucket,
    :bucket_width AS interval,
    MIN(COALESCE(device_data.long_v, 9223372036854775807)) AS long_value,
    MIN(COALESCE(device_data.double_v, 1.79769E+308)) AS double_value,
    MAX(device_data.ts) AS agg_values_last_ts
"""

FIND_SUM_QUERY: str = """
    SELECT
    time_bucket(:bucket_width, device_data.ts, :timezone, :start_date) AS bucket,
    :bucket_width AS interval,
    SUM(COALESCE(device_data.long_v, 0)) AS long_value,
    SUM(COALESCE(device_data.double_v, 0.0)) AS double_value,
    MAX(device_data.ts) AS agg_values_last_ts
"""

FIND_COUNT_QUERY: str = """
    SELECT
    time_bucket(:bucket_width, device_data.ts, :timezone, :start_date) AS bucket,
    :bucket_width AS interval,
    SUM(CASE WHEN device_data.bool_v IS NULL THEN 0 ELSE 1 END) AS count_bool_value,
    SUM(CASE WHEN device_data.str_v IS NULL THEN 0 ELSE 1 END) AS count_str_value,
    SUM(CASE WHEN device_data.long_v IS NULL THEN 0 ELSE 1 END) AS count_long_value,
    SUM(CASE WHEN device_data.double_v IS NULL THEN 0 ELSE 1 END) AS count_double_value,
    SUM(CASE WHEN device_data.json_v IS NULL THEN 0 ELSE 1 END) AS count_json_value,
    MAX(device_data.ts) AS agg_values_last_ts
"""
