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

TARGETS = list(RENAME_TARGETS_FEATURE_IMPORTANCES.keys())
TARGETS_TARGETS = [
    f"{target_1} vs {target_2}" for idx_target, target_1 in enumerate(TARGETS) for target_2 in TARGETS[idx_target:]
]

ALGORITHMS = ["elastic_net", "light_gbm"]
ALGORITHMS_ALGORITHMS = [
    f"{algorithm_1} vs {algorithm_2}"
    for idx_algorithm, algorithm_1 in enumerate(ALGORITHMS)
    for algorithm_2 in TARGETS[idx_algorithm:]
]

SCORES_SURVIVAL = {"c_index": "C-index", "diff_c_index": "Difference C-index"}
SCORES = {
    "age": {"r2": "r²", "rmse": "RMSE"},
    "all": SCORES_SURVIVAL,
    "cvd": SCORES_SURVIVAL,
    "cancer": SCORES_SURVIVAL,
}
