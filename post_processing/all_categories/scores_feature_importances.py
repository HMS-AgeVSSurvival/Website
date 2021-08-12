import pandas as pd
import numpy as np
from tqdm import tqdm

from website import MAIN_CATEGORIES, TARGETS, ALGORITHMS, FOLDS_FEATURE_IMPORTANCES
from post_processing import RANDOM_STATES, RENAME_TARGETS_FEATURE_IMPORTANCES, SCORES


LIST_ALGORITHMS = list(ALGORITHMS.keys())
LIST_ALGORITHMS.remove("best")


if __name__ == "__main__":
    list_new_scores = []
    for main_category in tqdm(MAIN_CATEGORIES):
        results_0 = pd.read_excel(
            "data/Results.xlsx", f"{main_category} {RANDOM_STATES[0]}", header=[0, 1, 2], index_col=[0]
        )
        results_1 = pd.read_excel(
            "data/Results.xlsx", f"{main_category} {RANDOM_STATES[1]}", header=[0, 1, 2], index_col=[0]
        )

        new_scores = pd.DataFrame(
            None,
            index=pd.MultiIndex.from_product((results_0.index.to_list(), LIST_ALGORITHMS)),
            columns=pd.MultiIndex.from_tuples([("age", "train", "r2")]),
        )

        for target in TARGETS:
            name_target = RENAME_TARGETS_FEATURE_IMPORTANCES[target]
            for algorithm in LIST_ALGORITHMS:
                for score in SCORES[target]:
                    name_score = SCORES[target][score]
                    if score == "diff_c_index":
                        continue
                    comparison = pd.DataFrame(None)
                    comparison[RANDOM_STATES[0]] = results_0[(name_target, algorithm, f"train {name_score}")]
                    comparison[RANDOM_STATES[1]] = results_1[(name_target, algorithm, f"train {name_score}")]
                    idx_best_0 = results_0.index[comparison.T.idxmax() == RANDOM_STATES[0]].to_list()
                    idx_best_1 = results_1.index[comparison.T.idxmax() == RANDOM_STATES[1]].to_list()

                    for fold in FOLDS_FEATURE_IMPORTANCES:
                        new_scores.loc[(idx_best_0, algorithm), (target, fold, score)] = results_0.loc[
                            idx_best_0, (name_target, algorithm, f"{fold} {name_score}")
                        ].values
                        new_scores.loc[(idx_best_1, algorithm), (target, fold, score)] = results_1.loc[
                            idx_best_1, (name_target, algorithm, f"{fold} {name_score}")
                        ].values
                        new_scores.loc[(idx_best_0, algorithm), (target, fold, f"{score}_std")] = results_0.loc[
                            idx_best_0, (name_target, algorithm, f"{fold} {name_score} std")
                        ].values
                        new_scores.loc[(idx_best_1, algorithm), (target, fold, f"{score}_std")] = results_1.loc[
                            idx_best_1, (name_target, algorithm, f"{fold} {name_score} std")
                        ].values
        list_new_scores.append(new_scores)

    merged_new_scores = pd.concat(
        list_new_scores, keys=MAIN_CATEGORIES.keys(), names=["main_category", "category", "algorithm"]
    )
    merged_new_scores.columns = map(str, merged_new_scores.columns.tolist())
    merged_new_scores.reset_index().to_feather("data/all_categories/scores_feature_importances.feather")
