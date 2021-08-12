import pandas as pd

from website import CUSTOM_CATEGORIES_INDEX


if __name__ == "__main__":
    scores_residual = pd.DataFrame(pd.read_feather("data/all_categories/scores_residual.feather")).set_index(
        ["main_category", "category", "algorithm"]
    )
    scores_residual.columns = pd.MultiIndex.from_tuples(
        list(map(eval, scores_residual.columns.tolist())), names=["target", "fold", "metric"]
    )

    custom_scores_residual = scores_residual.loc[
        (
            CUSTOM_CATEGORIES_INDEX.get_level_values("main_category"),
            CUSTOM_CATEGORIES_INDEX.get_level_values("category"),
        ),
        :,
    ]
    custom_scores_residual.columns = map(str, custom_scores_residual.columns.tolist())
    custom_scores_residual.reset_index().to_feather("data/custom_categories/scores_residual.feather")

    scores_feature_importances = pd.DataFrame(
        pd.read_feather("data/all_categories/scores_feature_importances.feather")
    ).set_index(["main_category", "category", "algorithm"])
    scores_feature_importances.columns = pd.MultiIndex.from_tuples(
        list(map(eval, scores_feature_importances.columns.tolist())), names=["target", "fold", "metric"]
    )

    custom_scores_feature_importances = scores_feature_importances.loc[
        (
            CUSTOM_CATEGORIES_INDEX.get_level_values("main_category"),
            CUSTOM_CATEGORIES_INDEX.get_level_values("category"),
        ),
        :,
    ]
    custom_scores_feature_importances.columns = map(str, custom_scores_feature_importances.columns.tolist())
    custom_scores_feature_importances.reset_index().to_feather(
        "data/custom_categories/scores_feature_importances.feather"
    )

    information = pd.DataFrame(pd.read_feather(f"data/all_categories/information.feather")).set_index(
        ["main_category", "category"]
    )
    information.columns = pd.MultiIndex.from_tuples(
        list(map(eval, information.columns.tolist())), names=["target", "information", "detail"]
    )

    custom_information = information.loc[CUSTOM_CATEGORIES_INDEX]
    custom_information.columns = map(str, custom_information.columns.tolist())
    custom_information.reset_index().to_feather("data/custom_categories/information.feather")
