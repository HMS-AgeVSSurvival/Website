RANDOM_STATES = [1, 2]

RENAME_TARGETS_RESIDUAL = {
    "age": "Age prediction",
    "all": "Survival all",
    "cvd": "Survival cvd",
    "cancer": "Survival cancer",
}
RENAME_TARGETS_FEATURE_IMPORTANCES = {
    "age": "Age feature importances",
    "all": "Survival all feature importances",
    "cvd": "Survival cvd feature importances",
    "cancer": "Survival cancer feature importances",
}

SCORES_SURVIVAL = {"c_index": "C-index", "diff_c_index": "Difference C-index"}
SCORES = {
    "age": {"r2": "r²", "rmse": "RMSE"},
    "all": SCORES_SURVIVAL,
    "cvd": SCORES_SURVIVAL,
    "cancer": SCORES_SURVIVAL,
}
