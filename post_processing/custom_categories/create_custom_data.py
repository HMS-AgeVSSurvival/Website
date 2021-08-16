import pandas as pd

from website import CUSTOM_CATEGORIES_INDEX, METHODS, TARGETS


if __name__ == "__main__":
    scores_residual = pd.DataFrame(pd.read_feather("data/all_categories/scores_residual.feather")).set_index(
        ["main_category", "category"]
    )
    custom_scores_residual = scores_residual.loc[CUSTOM_CATEGORIES_INDEX]
    custom_scores_residual.reset_index().to_feather("data/custom_categories/scores_residual.feather")

    scores_feature_importances = pd.DataFrame(
        pd.read_feather("data/all_categories/scores_feature_importances.feather")
    ).set_index(["main_category", "category"])
    custom_scores_feature_importances = scores_feature_importances.loc[CUSTOM_CATEGORIES_INDEX]
    custom_scores_feature_importances.reset_index().to_feather(
        "data/custom_categories/scores_feature_importances.feather"
    )

    information = pd.DataFrame(pd.read_feather(f"data/all_categories/information.feather")).set_index(
        ["main_category", "category"]
    )
    custom_information = information.loc[CUSTOM_CATEGORIES_INDEX]
    custom_information.reset_index().to_feather("data/custom_categories/information.feather")

    # for idx_target_row, target_row in enumerate(TARGETS):
    #     for target_column in list(TARGETS.keys())[idx_target_row:]:
    #         for method in METHODS:
    #             for std_path in ["", "_std"]:
    #                 path_correlations = f"data/all_categories/correlations/residual/{method}{std_path}_{target_row}_{target_column}.feather"

    #                 correlations = pd.read_feather(path_correlations).set_index(["main_category", "category"])
    #                 custom_correlations = correlations.loc[CUSTOM_CATEGORIES_INDEX]
    #                 custom_correlations.reset_index().to_feather(
    #                     f"data/custom_categories/correlations/residual/{method}{std_path}_{target_row}_{target_column}.feather"
    #                 )

    #         path_number_participants = (
    #             f"data/all_categories/correlations/residual/number_participants_{target_row}_{target_column}.feather"
    #         )

    #         number_participants = pd.read_feather(path_number_participants).set_index(["main_category", "category"])
    #         custom_number_participants = number_participants.loc[CUSTOM_CATEGORIES_INDEX]
    #         custom_number_participants.reset_index().to_feather(
    #             f"data/custom_categories/correlations/residual/number_participants_{target_row}_{target_column}.feather"
    #         )

    for method in METHODS:
        for feature_importances_correlations_type in ["between_targets", "between_algorithms"]:
            correlations = pd.read_feather(
                f"data/all_categories/correlations/feature_importances/{method}_{feature_importances_correlations_type}.feather"
            ).set_index(["main_category", "category"])
            custom_correlations = correlations.loc[CUSTOM_CATEGORIES_INDEX]
            custom_correlations.reset_index().to_feather(
                f"data/custom_categories/correlations/feature_importances/{method}_{feature_importances_correlations_type}.feather"
            )
