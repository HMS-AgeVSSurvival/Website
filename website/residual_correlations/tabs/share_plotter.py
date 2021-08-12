import pandas as pd
import numpy as np

from website.utils.rename import rename
from website import (
    MAIN_CATEGORIES,
    ALGORITHMS,
    SCORES_RESIDUAL,
    AXES,
    AXIS_ROW,
    AXIS_COLUMN,
    GRAPH_SIZE,
    TOO_MANY_CATEGORIES,
)


def plot_heatmap(
    correlations_data, correlations_std_data, number_participants_data, scores_data, *args, custom_categories=True
):
    import plotly.graph_objs as go
    from website.utils.graphs import heatmap_by_sorted_index, add_custom_legend_axis

    if custom_categories:
        from website import CUSTOM_CATEGORIES as CATEGORIES_IN_DATA
    else:
        from website import CATEGORIES as CATEGORIES_IN_DATA

    (
        examination_categories_row,
        examination_categories_column,
        laboratory_categories_row,
        laboratory_categories_column,
        questionnaire_categories_row,
        questionnaire_categories_column,
        algorithms_row,
        algorithms_column,
        target_row,
        target_column,
    ) = args

    if (
        len(examination_categories_row) + len(laboratory_categories_row) + len(questionnaire_categories_row) == 0
        or len(examination_categories_column) + len(laboratory_categories_column) + len(questionnaire_categories_column)
        == 0
    ):
        return "Please select a category", go.Figure()
    elif len(algorithms_row) == 0 or len(algorithms_column) == 0:
        return "Please select an algorithm", go.Figure()

    target = {AXIS_ROW: target_row, AXIS_COLUMN: target_column}
    categories_to_display = {
        AXIS_ROW: {
            "examination": examination_categories_row,
            "laboratory": laboratory_categories_row,
            "questionnaire": questionnaire_categories_row,
        },
        AXIS_COLUMN: {
            "examination": examination_categories_column,
            "laboratory": laboratory_categories_column,
            "questionnaire": questionnaire_categories_column,
        },
    }
    algorithms = {AXIS_ROW: algorithms_row, AXIS_COLUMN: algorithms_column}
    metrics = {AXIS_ROW: SCORES_RESIDUAL[target_row], AXIS_COLUMN: SCORES_RESIDUAL[target_column]}

    algorithms_to_look_at = {}
    indexes = {}

    for key_axis in AXES:
        if algorithms[key_axis] == ["best"]:
            algorithms_to_look_at[key_axis] = list(ALGORITHMS.keys())
            algorithms_to_look_at[key_axis].remove("best")
        else:
            algorithms_to_look_at[key_axis] = algorithms[key_axis]

        indexes_to_take = []
        for main_category in MAIN_CATEGORIES:
            if categories_to_display[key_axis][main_category] == ["all"]:
                categories_to_display[key_axis][main_category] = (
                    pd.Index(list(CATEGORIES_IN_DATA[main_category].keys())).drop("all").to_list()
                )
            indexes_to_take.extend(
                pd.MultiIndex.from_product(
                    ([main_category], categories_to_display[key_axis][main_category], algorithms_to_look_at[key_axis])
                ).to_list()
            )
        indexes[key_axis] = pd.MultiIndex.from_tuples(indexes_to_take, names=["main_category", "category", "algorithm"])
        if len(indexes[key_axis].droplevel("algorithm").drop_duplicates()) > TOO_MANY_CATEGORIES:
            return (
                "Please select less categories, the time required to load the graphs is going to be too long...",
                go.Figure(),
            )

    scores = pd.DataFrame(scores_data).set_index(["main_category", "category", "algorithm"])
    scores.columns = pd.MultiIndex.from_tuples(
        list(map(eval, scores.columns.tolist())), names=["target", "fold", "metric"]
    )

    indexes_algorithms = {}

    for key_axis in AXES:
        if algorithms[key_axis] == ["best"]:
            scores_grouped_by_categories = (
                scores.loc[indexes[key_axis]].reset_index().groupby(by=["main_category", "category"])
            )
            best_algorithms = list(
                map(
                    lambda group: group[1]
                    .set_index("algorithm")[(target[key_axis], "test", list(metrics[key_axis].keys())[0])]
                    .idxmax(),
                    scores_grouped_by_categories,
                )
            )
            best_algorithms = pd.Series(best_algorithms).replace(np.nan, algorithms_to_look_at[key_axis][0])
            indexes_algorithms[key_axis] = pd.MultiIndex.from_tuples(
                list(
                    zip(
                        indexes[key_axis]
                        .droplevel("algorithm")
                        .drop_duplicates()
                        .get_level_values("main_category")
                        .to_list(),
                        indexes[key_axis]
                        .droplevel("algorithm")
                        .drop_duplicates()
                        .get_level_values("category")
                        .to_list(),
                        best_algorithms.to_list(),
                    )
                ),
                names=["main_category", "category", "algorithm"],
            )

        else:
            indexes_algorithms[key_axis] = indexes[key_axis]

    correlations = pd.DataFrame(correlations_data).set_index(["main_category", "category", "algorithm"])
    correlations.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations.columns.tolist())), names=["main_category", "category", "algorithm"]
    )
    correlations_std = pd.DataFrame(correlations_std_data).set_index(["main_category", "category", "algorithm"])
    correlations_std.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations_std.columns.tolist())), names=["main_category", "category", "algorithm"]
    )
    number_participants = pd.DataFrame(number_participants_data).set_index(["main_category", "category"])
    number_participants.columns = pd.MultiIndex.from_tuples(
        list(map(eval, number_participants.columns.tolist())), names=["main_category", "category"]
    )

    correlations_to_display = correlations.loc[indexes_algorithms[AXIS_ROW], indexes_algorithms[AXIS_COLUMN]]
    correlations_std_to_display = correlations_std.loc[indexes_algorithms[AXIS_ROW], indexes_algorithms[AXIS_COLUMN]]
    number_participants_to_display = pd.DataFrame(
        None,
        index=pd.MultiIndex.from_tuples(indexes_algorithms[AXIS_ROW]),
        columns=pd.MultiIndex.from_tuples(indexes_algorithms[AXIS_COLUMN]),
    )
    number_participants_to_display = number_participants.loc[
        indexes_algorithms[AXIS_ROW].droplevel("algorithm"),
        indexes_algorithms[AXIS_COLUMN].droplevel("algorithm"),
    ]
    number_participants_to_display.index = indexes_algorithms[AXIS_ROW]
    number_participants_to_display.columns = indexes_algorithms[AXIS_COLUMN]

    scores_template = pd.DataFrame(None, index=indexes_algorithms[AXIS_ROW], columns=indexes_algorithms[AXIS_COLUMN])
    scores_to_display = {AXIS_ROW: scores_template.copy(), AXIS_COLUMN: scores_template.copy()}
    scores_std_to_display = {AXIS_ROW: scores_template.copy(), AXIS_COLUMN: scores_template.copy()}

    transposed_template = scores_template.T
    transposed_template[indexes_algorithms[AXIS_ROW]] = scores.loc[
        indexes_algorithms[AXIS_ROW], (target[AXIS_ROW], "test", list(metrics[AXIS_ROW].keys())[0])
    ]
    scores_to_display[AXIS_ROW] = transposed_template.T
    transposed_template = scores_template.T
    transposed_template[indexes_algorithms[AXIS_ROW]] = scores.loc[
        indexes_algorithms[AXIS_ROW], (target[AXIS_ROW], "test", f"{list(metrics[AXIS_ROW].keys())[0]}_std")
    ]
    scores_std_to_display[AXIS_ROW] = transposed_template.T

    scores_to_display[AXIS_COLUMN][indexes_algorithms[AXIS_COLUMN]] = scores.loc[
        indexes_algorithms[AXIS_COLUMN], (target[AXIS_COLUMN], "test", list(metrics[AXIS_COLUMN].keys())[0])
    ]
    scores_std_to_display[AXIS_COLUMN][indexes_algorithms[AXIS_COLUMN]] = scores.loc[
        indexes_algorithms[AXIS_COLUMN], (target[AXIS_COLUMN], "test", f"{list(metrics[AXIS_COLUMN].keys())[0]}_std")
    ]

    customdata_list = [
        correlations_std_to_display,
        scores_to_display[AXIS_ROW],
        scores_std_to_display[AXIS_ROW],
        scores_to_display[AXIS_COLUMN],
        scores_std_to_display[AXIS_COLUMN],
        number_participants_to_display,
    ]
    stacked_customdata = list(map(list, np.dstack(customdata_list)))
    customdata = pd.DataFrame(
        stacked_customdata, index=indexes_algorithms[AXIS_ROW], columns=indexes_algorithms[AXIS_COLUMN]
    )

    rename(correlations_to_display, custom_categories=custom_categories)
    rename(correlations_std_to_display, custom_categories=custom_categories)
    rename(customdata, custom_categories=custom_categories)

    hovertemplate = (
        "Correlation: %{z:.3f} +- %{customdata[0]:.3f} <br><br>"
        + list(AXES.values())[0]
        + ": %{y} <br> "
        + list(metrics[AXIS_ROW].values())[0]
        + " : %{customdata[1]:.3f} +- %{customdata[2]:.3f} <br><br>"
        + list(AXES.values())[1]
        + ": %{x} <br> "
        + list(metrics[AXIS_COLUMN].values())[0]
        + " : %{customdata[3]:.3f} +- %{customdata[4]:.3f}"
        + "<extra>%{customdata[5]} participants</extra>"
    )

    fig = heatmap_by_sorted_index(correlations_to_display, hovertemplate, customdata)

    fig = add_custom_legend_axis(fig, correlations_to_display.index, -120, -70, 0, horizontal=False)
    fig = add_custom_legend_axis(fig, correlations_to_display.columns, -120, -70, 0, horizontal=True)

    fig.update_layout(
        yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        width=GRAPH_SIZE,
        height=GRAPH_SIZE,
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
    )

    if correlations_to_display.shape[0] == 1 and correlations_to_display.shape[1] == 1:
        title = f"number of valid correlations {number_participants_to_display.notna().sum().sum()}"
    else:
        title = f"Average correlation = {correlations_to_display.mean().mean().round(3)} +- {pd.Series(correlations_to_display.values.flatten()).std().round(3)}, number of valid correlations {number_participants_to_display.notna().sum().sum()}"

    return title, fig
