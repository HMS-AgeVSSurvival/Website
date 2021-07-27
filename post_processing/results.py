import pandas as pd
import numpy as np

from website import TARGETS, MAIN_CATEGORIES, ALGORITHMS, FOLDS, SCORES
from post_processing import RANDOM_STATES


RENAME_TARGETS = {"age": "Age prediction", "all": "Survival all", "cvd": "Survival cvd", "cancer": "Survival cancer"}


list_new_results = []
for main_category in MAIN_CATEGORIES:
    results_0 = pd.read_excel(
        "data/Results.xlsx", f"{main_category} {RANDOM_STATES[0]}", header=[0, 1, 2], index_col=[0]
    )
    results_1 = pd.read_excel(
        "data/Results.xlsx", f"{main_category} {RANDOM_STATES[1]}", header=[0, 1, 2], index_col=[0]
    )

    new_results = pd.DataFrame(
        None,
        index=results_0.index,
        columns=pd.MultiIndex.from_tuples([("age", "numbers", "numbers", "n_participants")]),
    )

    for target in TARGETS:
        name_target = RENAME_TARGETS[target]

        new_results[(target, "numbers", "numbers", "n_participants")] = results_0[
            (name_target, "Shape after preprocessing", "n_participants")
        ]
        new_results[(target, "numbers", "numbers", "n_variables")] = results_0[
            (name_target, "Shape after preprocessing", "n_variables")
        ]
        new_results[(target, "age_ranges", "age_ranges", "min")] = results_0[(name_target, "Age range", "min")]
        new_results[(target, "age_ranges", "age_ranges", "max")] = results_0[(name_target, "Age range", "max")]

        for algorithm in ALGORITHMS:
            if algorithm == "best":
                continue
            for score in SCORES[target]:
                name_score = SCORES[target][score]
                if score != "diff_c_index":
                    comparison = pd.DataFrame(None)
                    comparison[RANDOM_STATES[0]] = results_0[(name_target, algorithm, f"test {name_score}")]
                    comparison[RANDOM_STATES[1]] = results_1[(name_target, algorithm, f"test {name_score}")]
                    idx_best_0 = comparison.T.idxmax() == RANDOM_STATES[0]
                    idx_best_1 = comparison.T.idxmax() == RANDOM_STATES[1]

                    for fold in FOLDS:
                        new_results.loc[idx_best_0, (target, algorithm, fold, score)] = results_0.loc[
                            idx_best_0, (name_target, algorithm, f"{fold} {name_score}")
                        ]
                        new_results.loc[idx_best_1, (target, algorithm, fold, score)] = results_1.loc[
                            idx_best_1, (name_target, algorithm, f"{fold} {name_score}")
                        ]
                        new_results.loc[idx_best_0, (target, algorithm, fold, f"{score}_std")] = results_0.loc[
                            idx_best_0, (name_target, algorithm, f"{fold} {name_score} std")
                        ]
                        new_results.loc[idx_best_1, (target, algorithm, fold, f"{score}_std")] = results_1.loc[
                            idx_best_1, (name_target, algorithm, f"{fold} {name_score} std")
                        ]
                else:  # score == "diff_c_index"
                    comparison = pd.DataFrame(None)
                    comparison[RANDOM_STATES[0]] = results_0[(f"Basic survival {target}", algorithm, "test C-index")]
                    comparison[RANDOM_STATES[1]] = results_1[(f"Basic survival {target}", algorithm, "test C-index")]
                    idx_best_0 = comparison.T.idxmax() == RANDOM_STATES[0]
                    idx_best_1 = comparison.T.idxmax() == RANDOM_STATES[1]

                    for fold in FOLDS:
                        new_results.loc[idx_best_0, (target, algorithm, fold, score)] = (
                            new_results.loc[idx_best_0, (target, algorithm, fold, "c_index")]
                            - results_0.loc[idx_best_0, (f"Basic survival {target}", algorithm, f"{fold} C-index")]
                        )

                        new_results.loc[idx_best_1, (target, algorithm, fold, score)] = (
                            new_results.loc[idx_best_1, (target, algorithm, fold, "c_index")]
                            - results_1.loc[idx_best_1, (f"Basic survival {target}", algorithm, f"{fold} C-index")]
                        )

                        new_results.loc[idx_best_0, (target, algorithm, fold, f"{score}_std")] = np.sqrt(
                            new_results.loc[idx_best_0, (target, algorithm, fold, "c_index_std")] ** 2
                            + results_0.loc[idx_best_0, (f"Basic survival {target}", algorithm, f"{fold} C-index std")]
                            ** 2
                        )

                        new_results.loc[idx_best_1, (target, algorithm, fold, f"{score}_std")] = np.sqrt(
                            new_results.loc[idx_best_1, (target, algorithm, fold, "c_index_std")] ** 2
                            + results_1.loc[idx_best_1, (f"Basic survival {target}", algorithm, f"{fold} C-index std")]
                            ** 2
                        )
    list_new_results.append(new_results)


merged_new_results = pd.concat(list_new_results, keys=MAIN_CATEGORIES.keys(), names=["main_category", "category"])
merged_new_results.columns = map(str, merged_new_results.columns.tolist())
merged_new_results.reset_index().to_feather("data/scores.feather")
