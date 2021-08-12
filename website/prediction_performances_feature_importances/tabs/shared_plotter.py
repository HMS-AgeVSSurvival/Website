import pandas as pd
import numpy as np

from website.utils.rename import rename
from website import TARGETS, MAIN_CATEGORIES, ALGORITHMS, FOLDS_FEATURE_IMPORTANCES, SCORES_FEATURE_IMPORTANCES


def plot_scores(
    scores_data,
    information_data,
    targets,
    examination_categories,
    laboratory_categories,
    questionnaire_categories,
    algorithms,
    metric,
    custom_categories=True,
):
    import plotly.graph_objs as go
    from website.utils.graphs import add_custom_legend_axis

    if custom_categories:
        from website import CUSTOM_CATEGORIES as CATEGORIES_IN_DATA
    else:
        from website import CATEGORIES as CATEGORIES_IN_DATA

    if len(targets) == 0:
        return "Please select a target", go.Figure()
    elif len(examination_categories) + len(laboratory_categories) + len(questionnaire_categories) == 0:
        return "Please select a category", go.Figure()
    elif len(algorithms) == 0:
        return "Please select an algorithm", go.Figure()

    scores_full = pd.DataFrame(scores_data).set_index(["main_category", "category", "algorithm"])
    scores_full.columns = pd.MultiIndex.from_tuples(
        list(map(eval, scores_full.columns.tolist())), names=["target", "fold", "metric"]
    )
    information_full = pd.DataFrame(information_data).set_index(["main_category", "category"])
    information_full.columns = pd.MultiIndex.from_tuples(
        list(map(eval, information_full.columns.tolist())), names=["target", "information", "detail"]
    )

    categories_to_display = {
        "examination": examination_categories,
        "laboratory": laboratory_categories,
        "questionnaire": questionnaire_categories,
    }

    if algorithms == ["best"]:
        algorithms_to_look_at = list(ALGORITHMS.keys())
        algorithms_to_look_at.remove("best")
    else:
        algorithms_to_look_at = algorithms

    list_indexes_to_take = []
    for main_category in MAIN_CATEGORIES:
        if categories_to_display[main_category] == ["all"]:
            categories_to_display[main_category] = (
                pd.Index(list(CATEGORIES_IN_DATA[main_category].keys())).drop("all").to_list()
            )
        list_indexes_to_take.extend(
            pd.MultiIndex.from_product(
                ([main_category], categories_to_display[main_category], algorithms_to_look_at)
            ).to_list()
        )
    indexes_to_take = pd.MultiIndex.from_tuples(list_indexes_to_take, names=["main_category", "category", "algorithm"])
    if not custom_categories and len(indexes_to_take.droplevel("algorithm").drop_duplicates()) > 70:
        return (
            "Please select less categories, the time required to load the graphs is going to be too long...",
            go.Figure(),
        )
    scores = scores_full.loc[
        indexes_to_take, (targets, list(FOLDS_FEATURE_IMPORTANCES.keys()), [metric, f"{metric}_std"])
    ]
    information = information_full.loc[indexes_to_take.droplevel("algorithm").drop_duplicates(), targets]

    rename(scores, columns=False, custom_categories=custom_categories)
    rename(information, algorithm=False, columns=False, custom_categories=custom_categories)

    indexes_target_best_algorithms = {}
    if algorithms == ["best"]:
        scores_grouped_by_categories = scores.reset_index().groupby(by=["main_category", "category"])

        for target in targets:
            best_algorithms = list(
                map(
                    lambda group: group[1].set_index("algorithm")[(target, "test", metric)].idxmax(),
                    scores_grouped_by_categories,
                )
            )
            best_algorithms = pd.Series(best_algorithms).replace(np.nan, ALGORITHMS[algorithms_to_look_at[0]])
            indexes_target_best_algorithms[target] = pd.MultiIndex.from_tuples(
                list(
                    zip(
                        information.index.get_level_values("main_category").to_list(),
                        information.index.get_level_values("category").to_list(),
                        best_algorithms.to_list(),
                    )
                ),
                names=["main_category", "category", "algorithm"],
            )

    if targets != ["age"]:
        scores.replace(-1, np.nan, inplace=True)
    hovertemplate = "%{x},<Br> score: %{y:.3f} +- %{customdata[0]:.3f}, %{customdata[1]} participants with %{customdata[2]} variables, age range %{customdata[3]} to %{customdata[4]} years old <extra>%{customdata[5]}</extra>"

    figures = {}
    titles = {}

    for fold in FOLDS_FEATURE_IMPORTANCES:
        scores_fold = scores.loc[:, (slice(None), fold)]

        if sum(scores_fold.notna().values.flatten()) == 0:
            return f"{FOLDS_FEATURE_IMPORTANCES[fold]} has no value to show", go.Figure(), "", go.Figure()
        if scores_fold.shape[0] > 1:
            titles[
                fold
            ] = f"{FOLDS_FEATURE_IMPORTANCES[fold]}, average {SCORES_FEATURE_IMPORTANCES[targets[0]][metric]} = {pd.Series(scores_fold.loc[:, (targets, fold, metric)].values.flatten()).mean().round(3)} +- {pd.Series(scores_fold.loc[:, (targets, fold, metric)].values.flatten()).std().round(3)}"
        else:
            titles[fold] = FOLDS_FEATURE_IMPORTANCES[fold]

        x_positions = pd.Series(np.arange(5, 10 * len(information.index) + 5, 10), index=information.index)

        figures[fold] = go.Figure()
        figures[fold].update_layout(
            xaxis={
                "tickvals": np.arange(5, 10 * len(information.index) + 5, 10),
                "ticktext": [" - ".join(elem) for elem in information.index],
            }
        )

        for target in targets:
            for algorithm in algorithms:
                if algorithm == "best":
                    indexes = indexes_target_best_algorithms[target]
                    algorithms_custom_data = indexes_target_best_algorithms[target].get_level_values("algorithm")
                else:
                    indexes = (slice(None), slice(None), ALGORITHMS[algorithm])
                    algorithms_custom_data = [ALGORITHMS[algorithm]] * len(information.index)

                customdata = np.dstack(
                    (
                        scores_fold.loc[indexes, (target, fold, f"{metric}_std")].values.flatten(),
                        information[(target, "numbers", "n_participants")].values.flatten(),
                        information[(target, "numbers", "n_variables")].values.flatten(),
                        information[(target, "age_ranges", "min")].values.flatten().astype(int),
                        information[(target, "age_ranges", "max")].values.flatten().astype(int),
                        algorithms_custom_data,
                    )
                )[0]

                figures[fold].add_bar(
                    x=x_positions.loc[information.index].values.flatten(),
                    y=scores_fold.loc[indexes, (target, fold, metric)],
                    error_y={
                        "array": scores_fold.loc[indexes, (target, fold, f"{metric}_std")],
                        "type": "data",
                    },
                    name=f"{TARGETS[target]} {ALGORITHMS[algorithm]}",
                    hovertemplate=hovertemplate,
                    customdata=customdata,
                )

        add_custom_legend_axis(
            figures[fold],
            information.index,
            -120 if metric == "rmse" else -1,
            -60 if metric == "rmse" else -0.5,
            min(scores_fold.loc[:, (targets, fold, metric)].min().min(), 0),
        )

        figures[fold].update_layout(
            yaxis={
                "title": SCORES_FEATURE_IMPORTANCES[targets[0]][metric],
                "showgrid": False,
                "zeroline": False,
                "showticklabels": True,
                "title_font": {"size": 45},
                "dtick": 12 if metric == "rmse" else 0.1,
                "tickfont_size": 20,
            },
            xaxis={"showgrid": False, "zeroline": False},
            height=800,
            margin={"l": 0, "r": 0, "b": 0, "t": 0},
            legend={"orientation": "h", "yanchor": "bottom", "font": {"size": 30}},
        )

    return titles["train"], figures["train"]
