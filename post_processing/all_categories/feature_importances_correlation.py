import pandas as pd
from tqdm import tqdm

from website import MAIN_CATEGORIES, METHODS
from post_processing import TARGETS, TARGETS_TARGETS, ALGORITHMS, ALGORITHMS_ALGORITHMS


if __name__ == "__main__":
    for method in tqdm(METHODS):
        list_new_correlations_between_targets = []
        list_new_correlations_between_algorithms = []

        for main_category in MAIN_CATEGORIES:
            if main_category == "laboratory":
                continue
            correlations = pd.read_feather(
                f"data/all_categories/correlations/feature_importances/{method}_{main_category}.feather"
            ).set_index("category")
            correlations.columns = pd.MultiIndex.from_tuples(
                list(map(eval, correlations.columns.tolist())), names=["correlation_type", "target", "algorithm"]
            )
            # TO REMOVE
            correlations.drop(
                columns=correlations.columns[
                    correlations.columns.get_level_values("correlation_type") != "same_target_same_algorithm"
                ],
                inplace=True,
            )
            correlations.columns = correlations.columns.droplevel("correlation_type")
            # TO REMOVE
            correlations_std = pd.read_feather(
                f"data/all_categories/correlations/feature_importances/{method}_std_{main_category}.feather"
            ).set_index("category")
            correlations_std.columns = pd.MultiIndex.from_tuples(
                list(map(eval, correlations_std.columns.tolist())), names=["correlation_type", "target", "algorithm"]
            )
            correlations_std.columns = correlations_std.columns
            # TO REMOVE
            correlations_std.drop(
                columns=correlations_std.columns[
                    correlations_std.columns.get_level_values("correlation_type") != "same_target_same_algorithm"
                ],
                inplace=True,
            )
            correlations_std.columns = correlations_std.columns.droplevel("correlation_type")
            # TO REMOVE

            new_correlations_between_targets = pd.DataFrame(
                None,
                index=pd.MultiIndex.from_product(
                    (ALGORITHMS, correlations.index.to_list()), names=["algorithms", "category"]
                ),
                columns=pd.MultiIndex.from_product((TARGETS_TARGETS, ["correlation", "std"])),
            )

            for target_vs_target in TARGETS_TARGETS:
                target_a, target_b = target_vs_target.split(" vs ")

                for algorithm in ALGORITHMS:
                    if target_a == target_b:
                        new_correlations_between_targets.loc[
                            algorithm, (target_vs_target, "correlation")
                        ] = correlations[(target_a, algorithm)].values
                        new_correlations_between_targets.loc[algorithm, (target_vs_target, "std")] = correlations_std[
                            (target_a, algorithm)
                        ].values
                    else:
                        new_correlations_between_targets.loc[
                            algorithm, (target_vs_target, "correlation")
                        ] = correlations[(target_vs_target, algorithm)].values
                        new_correlations_between_targets.loc[algorithm, (target_vs_target, "std")] = correlations_std[
                            (target_vs_target, algorithm)
                        ].values

            new_correlations_between_algorithms = pd.DataFrame(
                None,
                index=pd.MultiIndex.from_product(
                    (TARGETS, correlations.index.to_list()), names=["targets", "category"]
                ),
                columns=pd.MultiIndex.from_product((ALGORITHMS_ALGORITHMS, ["correlation", "std"])),
            )

            for algorithm_vs_algorithm in ALGORITHMS_ALGORITHMS:
                algorithm_a, algorithm_b = algorithm_vs_algorithm.split(" vs ")

                for target in TARGETS:
                    if algorithm_a == algorithm_b:
                        new_correlations_between_algorithms.loc[
                            target, (algorithm_vs_algorithm, "correlation")
                        ] = correlations[(target, algorithm_a)].values

                        new_correlations_between_algorithms.loc[
                            target, (algorithm_vs_algorithm, "std")
                        ] = correlations_std[(target, algorithm_a)].values
                    else:
                        new_correlations_between_algorithms.loc[
                            target, (algorithm_vs_algorithm, "correlation")
                        ] = correlations[(target, algorithm_vs_algorithm)].values

                        new_correlations_between_algorithms.loc[
                            target, (algorithm_vs_algorithm, "std")
                        ] = correlations_std[(target, algorithm_vs_algorithm)].values

            list_new_correlations_between_targets.append(new_correlations_between_targets.swaplevel())
            list_new_correlations_between_algorithms.append(new_correlations_between_algorithms.swaplevel())

        merged_new_correlations_between_targets = pd.concat(
            list_new_correlations_between_targets,
            keys=["examination", "questionnaire"],  #  TO REMOVE MAIN_CATEGORIES.keys(),
            names=["main_category", "category", "algorithm"],
        )
        merged_new_correlations_between_targets.columns = map(
            str, merged_new_correlations_between_targets.columns.tolist()
        )
        merged_new_correlations_between_targets.reset_index().to_feather(
            f"data/all_categories/correlations/feature_importances/{method}_between_targets.feather"
        )

        merged_new_correlations_between_algorithms = pd.concat(
            list_new_correlations_between_algorithms,
            keys=["examination", "questionnaire"],  #  TO REMOVE MAIN_CATEGORIES.keys(),
            names=["main_category", "category", "target"],
        )
        merged_new_correlations_between_algorithms.columns = map(
            str, merged_new_correlations_between_algorithms.columns.tolist()
        )
        merged_new_correlations_between_algorithms.reset_index().to_feather(
            f"data/all_categories/correlations/feature_importances/{method}_between_algorithms.feather"
        )
