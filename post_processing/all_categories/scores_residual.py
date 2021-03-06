import pandas as pd
import numpy as np
from tqdm import tqdm

from website import MAIN_CATEGORIES, TARGETS, ALGORITHMS, FOLDS_RESIDUAL
from post_processing import RANDOM_STATES, RENAME_TARGETS_RESIDUAL, SCORES


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
            index=results_0.index,
            columns=pd.MultiIndex.from_tuples([("age", LIST_ALGORITHMS[0], "train", "r2")]),
        )

        for target in TARGETS:
            name_target = RENAME_TARGETS_RESIDUAL[target]
            for algorithm in LIST_ALGORITHMS:
                for score in SCORES[target]:
                    name_score = SCORES[target][score]
                    if score != "diff_c_index":
                        comparison = pd.DataFrame(None)
                        comparison[RANDOM_STATES[0]] = results_0[(name_target, algorithm, f"test {name_score}")]
                        comparison[RANDOM_STATES[1]] = results_1[(name_target, algorithm, f"test {name_score}")]
                        idx_best_0 = results_0.index[comparison.T.idxmax() == RANDOM_STATES[0]].to_list()
                        idx_best_1 = results_1.index[comparison.T.idxmax() == RANDOM_STATES[1]].to_list()

                        for fold in FOLDS_RESIDUAL:
                            new_scores.loc[idx_best_0, (target, algorithm, fold, score)] = results_0.loc[
                                idx_best_0, (name_target, algorithm, f"{fold} {name_score}")
                            ].values
                            new_scores.loc[idx_best_1, (target, algorithm, fold, score)] = results_1.loc[
                                idx_best_1, (name_target, algorithm, f"{fold} {name_score}")
                            ].values
                            new_scores.loc[idx_best_0, (target, algorithm, fold, f"{score}_std")] = results_0.loc[
                                idx_best_0, (name_target, algorithm, f"{fold} {name_score} std")
                            ].values
                            new_scores.loc[idx_best_1, (target, algorithm, fold, f"{score}_std")] = results_1.loc[
                                idx_best_1, (name_target, algorithm, f"{fold} {name_score} std")
                            ].values
                    else:  # score == "diff_c_index"
                        comparison = pd.DataFrame(None)
                        comparison[RANDOM_STATES[0]] = results_0[
                            (f"Basic survival {target}", algorithm, "test C-index")
                        ]
                        comparison[RANDOM_STATES[1]] = results_1[
                            (f"Basic survival {target}", algorithm, "test C-index")
                        ]
                        idx_best_0 = results_0.index[comparison.T.idxmax() == RANDOM_STATES[0]]
                        idx_best_1 = results_1.index[comparison.T.idxmax() == RANDOM_STATES[1]]

                        for fold in FOLDS_RESIDUAL:
                            new_scores.loc[idx_best_0, (target, algorithm, fold, score)] = (
                                new_scores.loc[idx_best_0, (target, algorithm, fold, "c_index")].values
                                - results_0.loc[
                                    idx_best_0, (f"Basic survival {target}", algorithm, f"{fold} C-index")
                                ].values
                            )

                            new_scores.loc[idx_best_1, (target, algorithm, fold, score)] = (
                                new_scores.loc[idx_best_1, (target, algorithm, fold, "c_index")].values
                                - results_1.loc[
                                    idx_best_1, (f"Basic survival {target}", algorithm, f"{fold} C-index")
                                ].values
                            )

                            new_scores.loc[idx_best_0, (target, algorithm, fold, f"{score}_std")] = np.sqrt(
                                new_scores.loc[idx_best_0, (target, algorithm, fold, "c_index_std")].values ** 2
                                + results_0.loc[
                                    idx_best_0, (f"Basic survival {target}", algorithm, f"{fold} C-index std")
                                ].values
                                ** 2
                            )

                            new_scores.loc[idx_best_1, (target, algorithm, fold, f"{score}_std")] = np.sqrt(
                                new_scores.loc[idx_best_1, (target, algorithm, fold, "c_index_std")].values ** 2
                                + results_1.loc[
                                    idx_best_1, (f"Basic survival {target}", algorithm, f"{fold} C-index std")
                                ].values
                                ** 2
                            )
        list_new_scores.append(new_scores)

    merged_new_scores = pd.concat(list_new_scores, keys=MAIN_CATEGORIES.keys(), names=["main_category", "category"])
    merged_new_scores.replace(-1, np.nan, inplace=True)
    merged_new_scores.columns = map(str, merged_new_scores.columns.tolist())
    merged_new_scores.reset_index().to_feather("data/all_categories/scores_residual.feather")
