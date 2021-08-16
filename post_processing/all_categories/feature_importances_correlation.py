import pandas as pd
from tqdm import tqdm

from website import MAIN_CATEGORIES, METHODS
from post_processing import TARGETS, TARGETS_TARGETS, ALGORITHMS, ALGORITHMS_ALGORITHMS


if __name__ == "__main__":
    for method in tqdm(METHODS):
        list_new_correlations_between_targets = []
        list_new_correlations_between_algorithms = []

        for main_category in MAIN_CATEGORIES:
            correlations = pd.read_feather(
                f"data/all_categories/correlations/feature_importances/{method}_{main_category}.feather"
            ).set_index("category")
            correlations.columns = pd.MultiIndex.from_tuples(
                list(map(eval, correlations.columns.tolist())), names=["target", "algorithm"]
            )

            correlations_std = pd.read_feather(
                f"data/all_categories/correlations/feature_importances/{method}_std_{main_category}.feather"
            ).set_index("category")
            correlations_std.columns = pd.MultiIndex.from_tuples(
                list(map(eval, correlations_std.columns.tolist())), names=["target", "algorithm"]
            )
            correlations_std.columns = correlations_std.columns

            new_correlations_between_targets = pd.DataFrame(
                None,
                index=correlations.index,
                columns=pd.MultiIndex.from_product(
                    (TARGETS_TARGETS, ALGORITHMS, ["correlation", "std"]), names=["targets", "algorithm", "metric"]
                ),
            )

            for target_vs_target in TARGETS_TARGETS:
                target_a, target_b = target_vs_target.split(" vs ")

                for algorithm in ALGORITHMS:
                    if target_a == target_b:
                        new_correlations_between_targets[(target_vs_target, algorithm, "correlation")] = correlations[
                            (target_a, algorithm)
                        ]
                        new_correlations_between_targets[(target_vs_target, algorithm, "std")] = correlations_std[
                            (target_a, algorithm)
                        ]
                    else:
                        new_correlations_between_targets[(target_vs_target, algorithm, "correlation")] = correlations[
                            (target_vs_target, algorithm)
                        ]
                        new_correlations_between_targets[(target_vs_target, algorithm, "std")] = correlations_std[
                            (target_vs_target, algorithm)
                        ]

            new_correlations_between_algorithms = pd.DataFrame(
                None,
                index=correlations.index,
                columns=pd.MultiIndex.from_product(
                    (TARGETS, ALGORITHMS_ALGORITHMS, ["correlation", "std"]), names=["target", "algorithms", "metric"]
                ),
            )

            for algorithm_vs_algorithm in ALGORITHMS_ALGORITHMS:
                algorithm_a, algorithm_b = algorithm_vs_algorithm.split(" vs ")

                for target in TARGETS:
                    if algorithm_a == algorithm_b:
                        new_correlations_between_algorithms[
                            (target, algorithm_vs_algorithm, "correlation")
                        ] = correlations[(target, algorithm_a)]

                        new_correlations_between_algorithms[(target, algorithm_vs_algorithm, "std")] = correlations_std[
                            (target, algorithm_a)
                        ]
                    else:
                        new_correlations_between_algorithms[
                            (target, algorithm_vs_algorithm, "correlation")
                        ] = correlations[(target, algorithm_vs_algorithm)]

                        new_correlations_between_algorithms[(target, algorithm_vs_algorithm, "std")] = correlations_std[
                            (target, algorithm_vs_algorithm)
                        ]

            list_new_correlations_between_targets.append(new_correlations_between_targets)
            list_new_correlations_between_algorithms.append(new_correlations_between_algorithms)

        merged_new_correlations_between_targets = pd.concat(
            list_new_correlations_between_targets,
            keys=MAIN_CATEGORIES.keys(),
            names=["main_category", "category"],
        )
        merged_new_correlations_between_targets.columns = map(
            str, merged_new_correlations_between_targets.columns.tolist()
        )
        merged_new_correlations_between_targets.reset_index().to_feather(
            f"data/all_categories/correlations/feature_importances/{method}_between_targets.feather"
        )

        merged_new_correlations_between_algorithms = pd.concat(
            list_new_correlations_between_algorithms,
            keys=MAIN_CATEGORIES.keys(),
            names=["main_category", "category"],
        )
        merged_new_correlations_between_algorithms.columns = map(
            str, merged_new_correlations_between_algorithms.columns.tolist()
        )
        merged_new_correlations_between_algorithms.reset_index().to_feather(
            f"data/all_categories/correlations/feature_importances/{method}_between_algorithms.feather"
        )
