from sqlframe.base.function_alternatives import (  # noqa
    any_value_ignore_nulls_not_supported as any_value,
    e_literal as e,
    expm1_from_exp as expm1,
    log1p_from_log as log1p,
    rint_from_round as rint,
    bitwise_not_from_bitnot as bitwise_not,
    skewness_from_skew as skewness,
    isnan_using_equal as isnan,
    isnull_using_equal as isnull,
    nanvl_as_case as nanvl,
    percentile_approx_without_accuracy_and_max_array as percentile_approx,
    bround_using_half_even as bround,
    shiftleft_from_bitshiftleft as shiftleft,
    shiftright_from_bitshiftright as shiftright,
    struct_with_eq as struct,
    make_date_date_from_parts as make_date,
    date_add_no_date_sub as date_add,
    date_add_no_date_sub as dateadd,
    date_sub_by_date_add as date_sub,
    add_months_using_func as add_months,
    months_between_cast_as_date_cast_roundoff as months_between,
    last_day_with_cast as last_day,
    from_unixtime_from_timestamp as from_unixtime,
    unix_timestamp_from_extract as unix_timestamp,
    base64_from_base64_encode as base64,
    unbase64_from_base64_decode_string as unbase64,
    format_number_from_to_char as format_number,
    overlay_from_substr as overlay,
    levenshtein_edit_distance as levenshtein,
    split_with_split as split,
    regexp_extract_coalesce_empty_str as regexp_extract,
    hex_using_encode as hex,
    unhex_hex_decode_str as unhex,
    create_map_with_cast as create_map,
    array_contains_cast_variant as array_contains,
    arrays_overlap_as_plural as arrays_overlap,
    slice_as_array_slice as slice,
    array_join_no_null_replacement as array_join,
    array_position_cast_variant_and_flip as array_position,
    element_at_using_brackets as element_at,
    array_intersect_using_intersection as array_intersect,
    array_union_using_array_concat as array_union,
    sort_array_using_array_sort as sort_array,
    flatten_using_array_flatten as flatten,
    map_concat_using_map_cat as map_concat,
    sequence_from_array_generate_range as sequence,
    to_number_using_to_double as to_number,
)
from sqlframe.base.functions import (
    abs as abs,
    acos as acos,
    acosh as acosh,
    approxCountDistinct as approxCountDistinct,
    approx_count_distinct as approx_count_distinct,
    array as array,
    array_distinct as array_distinct,
    array_except as array_except,
    array_max as array_max,
    array_min as array_min,
    array_remove as array_remove,
    array_sort as array_sort,
    asc as asc,
    asc_nulls_first as asc_nulls_first,
    asc_nulls_last as asc_nulls_last,
    ascii as ascii,
    asin as asin,
    asinh as asinh,
    atan as atan,
    atan2 as atan2,
    atanh as atanh,
    avg as avg,
    bit_length as bit_length,
    bitwiseNOT as bitwiseNOT,
    bool_and as bool_and,
    bool_or as bool_or,
    call_function as call_function,
    cbrt as cbrt,
    ceil as ceil,
    ceiling as ceiling,
    char as char,
    coalesce as coalesce,
    col as col,
    collect_list as collect_list,
    collect_set as collect_set,
    concat as concat,
    concat_ws as concat_ws,
    corr as corr,
    cos as cos,
    cosh as cosh,
    cot as cot,
    count as count,
    countDistinct as countDistinct,
    count_distinct as count_distinct,
    count_if as count_if,
    covar_pop as covar_pop,
    covar_samp as covar_samp,
    cume_dist as cume_dist,
    current_date as current_date,
    current_timestamp as current_timestamp,
    current_user as current_user,
    date_diff as date_diff,
    date_format as date_format,
    date_trunc as date_trunc,
    datediff as datediff,
    dayofmonth as dayofmonth,
    dayofweek as dayofweek,
    dayofyear as dayofyear,
    degrees as degrees,
    dense_rank as dense_rank,
    desc as desc,
    desc_nulls_first as desc_nulls_first,
    desc_nulls_last as desc_nulls_last,
    exp as exp,
    explode as explode,
    expr as expr,
    extract as extract,
    factorial as factorial,
    floor as floor,
    greatest as greatest,
    grouping_id as grouping_id,
    hash as hash,
    hour as hour,
    ifnull as ifnull,
    initcap as initcap,
    input_file_name as input_file_name,
    instr as instr,
    kurtosis as kurtosis,
    lag as lag,
    lcase as lcase,
    lead as lead,
    least as least,
    left as left,
    length as length,
    lit as lit,
    ln as ln,
    locate as locate,
    log as log,
    log10 as log10,
    log2 as log2,
    lower as lower,
    lpad as lpad,
    ltrim as ltrim,
    map_keys as map_keys,
    max as max,
    max_by as max_by,
    md5 as md5,
    mean as mean,
    min as min,
    min_by as min_by,
    minute as minute,
    month as month,
    next_day as next_day,
    now as now,
    nth_value as nth_value,
    ntile as ntile,
    nullif as nullif,
    nvl as nvl,
    nvl2 as nvl2,
    octet_length as octet_length,
    percent_rank as percent_rank,
    percentile as percentile,
    posexplode as posexplode,
    position as position,
    pow as pow,
    power as power,
    quarter as quarter,
    radians as radians,
    rand as rand,
    rank as rank,
    regexp_replace as regexp_replace,
    repeat as repeat,
    right as right,
    round as round,
    row_number as row_number,
    rpad as rpad,
    rtrim as rtrim,
    second as second,
    sha as sha,
    sha1 as sha1,
    sha2 as sha2,
    shiftLeft as shiftLeft,
    shiftRight as shiftRight,
    sign as sign,
    signum as signum,
    sin as sin,
    sinh as sinh,
    size as size,
    soundex as soundex,
    sqrt as sqrt,
    startswith as startswith,
    stddev as stddev,
    stddev_pop as stddev_pop,
    stddev_samp as stddev_samp,
    substring as substring,
    sum as sum,
    sumDistinct as sumDistinct,
    sum_distinct as sum_distinct,
    tan as tan,
    tanh as tanh,
    timestamp_seconds as timestamp_seconds,
    toDegrees as toDegrees,
    toRadians as toRadians,
    to_date as to_date,
    to_timestamp as to_timestamp,
    translate as translate,
    trim as trim,
    trunc as trunc,
    ucase as ucase,
    unix_date as unix_date,
    upper as upper,
    user as user,
    var_pop as var_pop,
    var_samp as var_samp,
    variance as variance,
    weekofyear as weekofyear,
    when as when,
    year as year,
)
