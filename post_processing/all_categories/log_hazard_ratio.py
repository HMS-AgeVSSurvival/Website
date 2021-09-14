import pandas as pd
import numpy as np
from tqdm import tqdm

from website import MAIN_CATEGORIES, ALGORITHMS
from post_processing import RANDOM_STATES, LOG_HAZARD_RATIO_METRIC


LIST_ALGORITHMS = list(ALGORITHMS.keys())
LIST_ALGORITHMS.remove("best")


if __name__ == "__main__":
    list_new_log_hazard_ratio = []
    for main_category in tqdm(MAIN_CATEGORIES):
        results_0 = pd.read_excel(
            "data/Results.xlsx", f"{main_category} {RANDOM_STATES[0]}", header=[0, 1, 2], index_col=[0]
        )
        results_1 = pd.read_excel(
            "data/Results.xlsx", f"{main_category} {RANDOM_STATES[1]}", header=[0, 1, 2], index_col=[0]
        )

        new_log_hazard_ratio = pd.DataFrame(
            None,
            index=results_0.index,
            columns=pd.MultiIndex.from_tuples([(list(ALGORITHMS.keys())[0], "log_hazard_ratio")]),
        )

        for algorithm in LIST_ALGORITHMS:
            comparison = pd.DataFrame(None)
            comparison[RANDOM_STATES[0]] = results_0[
                ("Survival from age residual", algorithm, LOG_HAZARD_RATIO_METRIC["p_value"])
            ]
            comparison[RANDOM_STATES[1]] = results_1[
                ("Survival from age residual", algorithm, LOG_HAZARD_RATIO_METRIC["p_value"])
            ]
            idx_best_0 = results_0.index[comparison.T.idxmin() == RANDOM_STATES[0]].to_list()
            idx_best_1 = results_1.index[comparison.T.idxmin() == RANDOM_STATES[1]].to_list()

            for metric in LOG_HAZARD_RATIO_METRIC:
                new_log_hazard_ratio.loc[idx_best_0, (algorithm, metric)] = results_0.loc[
                    idx_best_0, ("Survival from age residual", algorithm, LOG_HAZARD_RATIO_METRIC[metric])
                ].values
                new_log_hazard_ratio.loc[idx_best_1, (algorithm, metric)] = results_1.loc[
                    idx_best_1, ("Survival from age residual", algorithm, LOG_HAZARD_RATIO_METRIC[metric])
                ].values
        list_new_log_hazard_ratio.append(new_log_hazard_ratio)

    merged_new_log_hazard_ratio = pd.concat(
        list_new_log_hazard_ratio, keys=MAIN_CATEGORIES.keys(), names=["main_category", "category"]
    )
    merged_new_log_hazard_ratio.replace(-1, np.nan, inplace=True)
    merged_new_log_hazard_ratio.columns = map(str, merged_new_log_hazard_ratio.columns.tolist())
    merged_new_log_hazard_ratio.reset_index().to_feather("data/all_categories/log_hazard_ratio.feather")
