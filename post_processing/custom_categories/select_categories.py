import pandas as pd
import numpy as np


def objective_from_metrics(metrics):
    list_scores = [metrics[("age", "test", "r2")] - metrics[("age", "test", "r2_std")]] * 6

    for target in ["all", "cvd", "cancer"]:
        list_scores.append(metrics[(target, "test", "c_index")] - metrics[(target, "test", "c_index_std")] - 0.5)
        list_scores.append(
            (metrics[(target, "test", "diff_c_index")] - metrics[(target, "test", "diff_c_index_std")]) * 25
        )

    return pd.Series(list_scores).sum()


if __name__ == "__main__":
    scores = pd.DataFrame(pd.read_feather("data/scores.feather")).set_index(["main_category", "category", "algorithm"])
    scores.columns = pd.MultiIndex.from_tuples(
        list(map(eval, scores.columns.tolist())), names=["target", "fold", "metric"]
    )

    scores_algorithm_indexed = scores.swaplevel(0, 2).swaplevel()

    list_objectives = []

    for algorithm in scores_algorithm_indexed.index.get_level_values("algorithm").drop_duplicates():
        list_objectives.append(
            scores_algorithm_indexed.loc[algorithm].apply(
                lambda metrics: objective_from_metrics(metrics), axis="columns"
            )
        )

    objectives = pd.concat(list_objectives)
    objectives.sort_values(ascending=False, inplace=True)

    print(sorted(objectives.index.drop_duplicates()[:30].to_list()))
