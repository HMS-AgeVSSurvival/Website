import pandas as pd

from website import CUSTOM_CATEGORIES_INDEX


if __name__ == "__main__":
    scores = pd.DataFrame(pd.read_feather("data/all_categories/scores_residual.feather")).set_index(
        ["main_category", "category", "algorithm"]
    )
    scores.columns = pd.MultiIndex.from_tuples(
        list(map(eval, scores.columns.tolist())), names=["target", "fold", "metric"]
    )

    custom_scores = scores.loc[
        (
            CUSTOM_CATEGORIES_INDEX.get_level_values("main_category"),
            CUSTOM_CATEGORIES_INDEX.get_level_values("category"),
        ),
        :,
    ]
    custom_scores.columns = map(str, custom_scores.columns.tolist())
    custom_scores.reset_index().to_feather("data/custom_categories/scores_residual.feather")

    information = pd.DataFrame(pd.read_feather(f"data/all_categories/information.feather")).set_index(
        ["main_category", "category"]
    )
    information.columns = pd.MultiIndex.from_tuples(
        list(map(eval, information.columns.tolist())), names=["target", "information", "detail"]
    )

    custom_information = information.loc[CUSTOM_CATEGORIES_INDEX]
    custom_information.columns = map(str, custom_information.columns.tolist())
    custom_information.reset_index().to_feather("data/custom_categories/information.feather")
