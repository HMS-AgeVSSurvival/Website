import pandas as pd
from tqdm import tqdm

from website import TARGETS, MAIN_CATEGORIES, ALGORITHMS
from post_processing import RANDOM_STATES, RENAME_TARGETS_RESIDUAL


LIST_ALGORITHMS = list(ALGORITHMS.keys())
LIST_ALGORITHMS.remove("best")


if __name__ == "__main__":
    list_new_information = []
    for main_category in tqdm(MAIN_CATEGORIES):
        results_0 = pd.read_excel(
            "data/Results.xlsx", f"{main_category} {RANDOM_STATES[0]}", header=[0, 1, 2], index_col=[0]
        )

        new_information = pd.DataFrame(
            None,
            index=results_0.index,
            columns=pd.MultiIndex.from_tuples([("age", "numbers", "n_participants")]),
        )

        for target in TARGETS:
            name_target = RENAME_TARGETS_RESIDUAL[target]

            new_information[(target, "numbers", "n_participants")] = results_0[
                (name_target, "Shape after preprocessing", "n_participants")
            ]
            new_information[(target, "numbers", "n_variables")] = results_0[
                (name_target, "Shape after preprocessing", "n_variables")
            ]
            new_information[(target, "age_ranges", "min")] = results_0[(name_target, "Age range", "min")]
            new_information[(target, "age_ranges", "max")] = results_0[(name_target, "Age range", "max")]

        list_new_information.append(new_information)

    merged_new_information = pd.concat(
        list_new_information, keys=MAIN_CATEGORIES.keys(), names=["main_category", "category"]
    )
    merged_new_information.columns = map(str, merged_new_information.columns.tolist())
    merged_new_information.reset_index().to_feather("data/all_categories/information.feather")
