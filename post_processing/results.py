import pandas as pd

from website import TARGETS, CATEGORIES, MAIN_CATEGORIES, ALGORITHMS, FOLDS, SCORES
from post_processing import DATA_INFORMATION, RANDOM_STATES

# list_indexes = []
# for main_category in MAIN_CATEGORIES:
#     for category in CATEGORIES[main_category]:
#         if category == "all":
#             continue
#         list_indexes.append([main_category, category])

# list_columns = []
# for target in TARGETS:
#     for data_information_type in DATA_INFORMATION:
#         for data_information in DATA_INFORMATION[data_information_type]:
#             # Repete "data_information_type" to match the other columns
#             list_columns.append([target, data_information_type, data_information_type, data_information])
#     for fold in FOLDS:
#         for algorithm in ALGORITHMS:
#             for score in SCORES[target]:
#                 list_columns.append([target, algorithm, fold, score])
#                 list_columns.append([target, algorithm, fold, f"{score}_std"])

# indexes = pd.MultiIndex.from_tuples(list_indexes)
# columns = pd.MultiIndex.from_tuples(list_columns)
# merged_results = pd.DataFrame(None, index=indexes, columns=columns)

RENAME_TARGETS = {"Age prediction": "age", "Survival all": "all", "Survival cvd": "cvd", "Survival cancer": "cancer"}
RENAME_INFORMATION = {"Shape after preprocessing": "numbers", "Age range": "age_ranges"}
RENAME_SCORES = {
    "r²": "r2",
    "r² std": "r2_std",
    "RMSE": "rmse",
    "RMSE std": "rmse_std",
    "C-index": "c_index",
    "C-index std": "c_index_std",
}

results_0 = pd.read_excel("data/Results.xlsx", f"examination {RANDOM_STATES[0]}", header=[0, 1, 2], index_col=[0])
list_new_columns = []
list_former_columns = []
for levels_column in results_0.columns:
    if (
        levels_column[0] in RENAME_TARGETS.keys() and levels_column[2][-2:] != ".1"
    ):  # .1 is how pandas interprets the separations
        list_former_columns.append(levels_column)

        new_column = [RENAME_TARGETS[levels_column[0]]]
        if levels_column[1] in RENAME_INFORMATION.keys():
            new_column.append(RENAME_INFORMATION[levels_column[1]])
            new_column.append(RENAME_INFORMATION[levels_column[1]])  # Twice to match with the scores depth
            new_column.append(levels_column[2])
        else:
            new_column.append(levels_column[1])
            if "train" in levels_column[2]:
                new_column.append("train")
                new_column.append(RENAME_SCORES[levels_column[2][6:]])  # "5" for test "+1" for space
            else:
                new_column.append("test")
                new_column.append(RENAME_SCORES[levels_column[2][5:]])  # "4" for test "+1" for space

        list_new_columns.append(new_column)

former_columns = pd.MultiIndex.from_tuples(list_former_columns)
new_columns = pd.MultiIndex.from_tuples(list_new_columns)
new_results_0 = results_0[former_columns]
new_results_0.columns = new_columns
print(new_results_0)
#     for target in TARGETS:
#         if target == "age":
#             title_target = "Age prediction"
#         else:
#             title_target = f"Survival {target}"

#         merged_results.loc[
#             main_category,
#             [
#                 (target, "numbers", "numbers", "n_participants"),
#                 (target, "numbers", "numbers", "n_variables"),
#                 (target, "age_ranges", "age_ranges", "min"),
#                 (target, "age_ranges", "age_ranges", "max"),
#             ],
#         ] = results_0.loc[
#             merged_results.loc[main_category].index,
#             [
#                 (title_target, "Shape after preprocessing", "n_participants"),
#                 (title_target, "Shape after preprocessing", "n_variables"),
#                 (title_target, "Age range", "min"),
#                 (title_target, "Age range", "max"),
#             ],
#         ].values

#         for fold in FOLDS:
#             for algorithm in ALGORITHMS:
#                 for score in SCORES[target]:
#                     merged_results.loc[
#                         main_category,
#                         [(target, algorithm, fold, score), (target, algorithm, fold, f"{score}_std")],
#                     ] = results_0[
#                         [
#                             (title_target, algorithm, f"{fold} {SCORES[target][score]}"),
#                             (title_target, algorithm, f"{fold} {SCORES[target][score]} std"),
#                         ]
#                     ]
#                     break
#                 break
#             break
#         break
#     break
# print(merged_results)
