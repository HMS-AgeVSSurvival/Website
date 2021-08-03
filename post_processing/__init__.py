RANDOM_STATES = [1, 2]

RENAME_TARGETS = {"age": "Age prediction", "all": "Survival all", "cvd": "Survival cvd", "cancer": "Survival cancer"}

SCORES_SURVIVAL = {"c_index": "C-index", "diff_c_index": "Difference C-index"}
SCORES = {
    "age": {"r2": "r²", "rmse": "RMSE"},
    "all": SCORES_SURVIVAL,
    "cvd": SCORES_SURVIVAL,
    "cancer": SCORES_SURVIVAL,
}
