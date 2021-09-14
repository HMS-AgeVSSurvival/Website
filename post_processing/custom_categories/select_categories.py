import pandas as pd
import numpy as np

from post_processing import ALGORITHMS, TARGETS

CATEGORIES_TO_SELECT = 30


def objective_function(metrics):
    best_scores = pd.Series(None, index=TARGETS, dtype=np.float32)
    for target in TARGETS:
        metric = "r2" if target == "age" else "diff_c_index"
        best_scores.loc[target] = (
            metrics.loc[(target, ALGORITHMS, "test", metric)]
            - metrics.loc[(target, ALGORITHMS, "test", f"{metric}_std")].values
        ).max()

    return best_scores


if __name__ == "__main__":
    scores = pd.DataFrame(pd.read_feather("data/all_categories/scores_residual.feather")).set_index(
        ["main_category", "category"]
    )
    scores.columns = pd.MultiIndex.from_tuples(
        list(map(eval, scores.columns.tolist())), names=["target", "algorithm", "fold", "metric"]
    )

    best_scores_counting_std = scores.apply(objective_function, axis="columns")
    rank_scores = best_scores_counting_std.apply(lambda scores: scores.rank(ascending=False, na_option="bottom"))
    rank_scores["age"] *= 3

    ranked_categories = rank_scores.sum(axis=1).sort_values().index
    print("Updated list:")
    print(sorted(ranked_categories.values[:CATEGORIES_TO_SELECT]))
    print("\nBest model not taken")
    print(scores.loc[ranked_categories[CATEGORIES_TO_SELECT]].to_frame())
