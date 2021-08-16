from re import L
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


def get_indexes(
    scores,
    target,
    examination_categories,
    laboratory_categories,
    questionnaire_categories,
    algorithms,
    categories_in_data,
):
    if examination_categories == ["all"]:
        examination_categories = list(categories_in_data["examination"].keys())
        examination_categories.remove("all")
    if laboratory_categories == ["all"]:
        laboratory_categories = list(categories_in_data["laboratory"].keys())
        laboratory_categories.remove("all")
    if questionnaire_categories == ["all"]:
        questionnaire_categories = list(categories_in_data["questionnaire"].keys())
        questionnaire_categories.remove("all")

    list_categories_to_take = []
    list_categories_to_take.append(pd.MultiIndex.from_product((["examination"], examination_categories)).to_frame())
    list_categories_to_take.append(pd.MultiIndex.from_product((["laboratory"], laboratory_categories)).to_frame())
    list_categories_to_take.append(pd.MultiIndex.from_product((["questionnaire"], questionnaire_categories)).to_frame())
    categories_to_take = pd.concat(list_categories_to_take)
    categories_to_take.columns = ["main_category", "category"]

    if algorithms == ["best"]:
        metric = list(SCORES_RESIDUAL[target].keys())[0]

        best_algorithms = (
            scores.loc[categories_to_take.index, (target, slice(None), "test", metric)]
            .droplevel(["target", "fold", "metric"], axis=1)
            .idxmax(axis=1)
        ).replace(np.nan, list(ALGORITHMS.values())[0])
        return pd.MultiIndex.from_tuples(
            best_algorithms.reset_index().apply(lambda x: tuple(x), axis=1),
            names=["main_category", "category", "algorithm"],
        )

    else:
        indexes_to_take = pd.concat(
            [categories_to_take] * len(algorithms), keys=algorithms, names=["algorithm", "main_category", "category"]
        )
        return indexes_to_take.swaplevel().swaplevel(i=0, j=2).sort_index().index


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
        target_row,
        target_column,
        examination_categories_row,
        examination_categories_column,
        laboratory_categories_row,
        laboratory_categories_column,
        questionnaire_categories_row,
        questionnaire_categories_column,
        algorithms_row,
        algorithms_column,
    ) = args

    if (
        len(examination_categories_row) + len(laboratory_categories_row) + len(questionnaire_categories_row) == 0
        or len(examination_categories_column) + len(laboratory_categories_column) + len(questionnaire_categories_column)
        == 0
    ):
        return "Please select a category", go.Figure()
    elif len(algorithms_row) == 0 or len(algorithms_column) == 0:
        return "Please select an algorithm", go.Figure()

    scores = pd.DataFrame(scores_data).set_index(["main_category", "category"])
    scores.columns = pd.MultiIndex.from_tuples(
        list(map(eval, scores.columns.tolist())), names=["target", "algorithm", "fold", "metric"]
    )
    indexes_row = get_indexes(
        scores,
        target_row,
        examination_categories_row,
        laboratory_categories_row,
        questionnaire_categories_row,
        algorithms_row,
        CATEGORIES_IN_DATA,
    )
    if len(indexes_row.droplevel("algorithm").drop_duplicates()) > TOO_MANY_CATEGORIES:
        return (
            "Please select less categories, the time required to load the graphs is going to be too long...",
            go.Figure(),
        )
    indexes_columns = get_indexes(
        scores,
        target_column,
        examination_categories_column,
        laboratory_categories_column,
        questionnaire_categories_column,
        algorithms_column,
        CATEGORIES_IN_DATA,
    )
    if len(indexes_columns.droplevel("algorithm").drop_duplicates()) > TOO_MANY_CATEGORIES:
        return (
            "Please select less categories, the time required to load the graphs is going to be too long...",
            go.Figure(),
        )
    correlations = (
        pd.DataFrame(correlations_data).set_index(["main_category", "category", "algorithm"]).loc[indexes_row]
    )
    correlations.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations.columns.tolist())), names=["main_category", "category", "algorithm"]
    )
    correlations = correlations[indexes_columns]
    correlations_std = (
        pd.DataFrame(correlations_std_data).set_index(["main_category", "category", "algorithm"]).loc[indexes_row]
    )
    correlations_std.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations_std.columns.tolist())), names=["main_category", "category", "algorithm"]
    )
    correlations_std = correlations_std[indexes_columns]
    number_participants = (
        pd.DataFrame(number_participants_data)
        .set_index(["main_category", "category"])
        .loc[indexes_row.droplevel("algorithm")]
    )
    number_participants.columns = pd.MultiIndex.from_tuples(
        list(map(eval, number_participants.columns.tolist())), names=["main_category", "category"]
    )
    number_participants = number_participants[indexes_columns.droplevel("algorithm")]
    number_participants.index = indexes_row
    number_participants.columns = indexes_columns

    metric_row = list(SCORES_RESIDUAL[target_row].keys())[0]
    metric_columns = list(SCORES_RESIDUAL[target_column].keys())[0]

    scores_template = pd.DataFrame(None, index=indexes_row, columns=indexes_columns)
    scores_to_display = {AXIS_ROW: scores_template.copy(), AXIS_COLUMN: scores_template.copy()}
    scores_std_to_display = {AXIS_ROW: scores_template.copy(), AXIS_COLUMN: scores_template.copy()}

    stacked_scores = scores.loc[
        :,
        (
            [target_row, target_column],
            slice(None),
            "test",
            [metric_row, f"{metric_row}_std", metric_columns, f"{metric_columns}_std"],
        ),
    ].stack(level="algorithm", dropna=False)

    transposed_template = scores_template.T
    transposed_template[indexes_row] = stacked_scores.loc[indexes_row, (target_row, "test", metric_row)]
    scores_to_display[AXIS_ROW] = transposed_template.T

    transposed_template = scores_template.T
    transposed_template[indexes_row] = stacked_scores.loc[indexes_row, (target_row, "test", f"{metric_row}_std")]
    scores_std_to_display[AXIS_ROW] = transposed_template.T

    scores_to_display[AXIS_COLUMN][indexes_columns] = stacked_scores.loc[
        indexes_columns, (target_column, "test", metric_columns)
    ]
    scores_std_to_display[AXIS_COLUMN][indexes_columns] = stacked_scores.loc[
        indexes_columns, (target_column, "test", f"{metric_columns}_std")
    ]

    customdata_list = [
        correlations_std,
        scores_to_display[AXIS_ROW],
        scores_std_to_display[AXIS_ROW],
        scores_to_display[AXIS_COLUMN],
        scores_std_to_display[AXIS_COLUMN],
        number_participants,
    ]
    stacked_customdata = list(map(list, np.dstack(customdata_list)))
    customdata = pd.DataFrame(stacked_customdata, index=indexes_row, columns=indexes_columns)

    rename(
        correlations,
        index_main_category=True,
        index_category=True,
        index_algorithm=True,
        columns_main_category=True,
        columns_category=True,
        columns_algorithm=True,
        custom_categories=custom_categories,
    )
    rename(
        correlations_std,
        index_main_category=True,
        index_category=True,
        index_algorithm=True,
        columns_main_category=True,
        columns_category=True,
        columns_algorithm=True,
        custom_categories=custom_categories,
    )
    rename(
        customdata,
        index_main_category=True,
        index_category=True,
        index_algorithm=True,
        columns_main_category=True,
        columns_category=True,
        columns_algorithm=True,
        custom_categories=custom_categories,
    )
    hovertemplate = (
        "Correlation: %{z:.3f} +- %{customdata[0]:.3f} <br><br>"
        + list(AXES.values())[0]
        + ": %{y} <br> "
        + metric_row
        + " : %{customdata[1]:.3f} +- %{customdata[2]:.3f} <br><br>"
        + list(AXES.values())[1]
        + ": %{x} <br> "
        + metric_columns
        + " : %{customdata[3]:.3f} +- %{customdata[4]:.3f}"
        + "<extra>%{customdata[5]} participants</extra>"
    )

    fig = heatmap_by_sorted_index(correlations, hovertemplate, customdata)

    fig = add_custom_legend_axis(fig, correlations.index, -120, -70, 0, horizontal=False)
    fig = add_custom_legend_axis(fig, correlations.columns, -120, -70, 0, horizontal=True)

    fig.update_layout(
        yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        width=GRAPH_SIZE,
        height=GRAPH_SIZE,
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
    )

    if correlations.shape[0] == 1 and correlations.shape[1] == 1:
        title = f"number of valid correlations {sum(number_participants.notna().values.flatten())}"
    else:
        title = f"Average correlation = {pd.Series(correlations.values.flatten()).mean().round(3)} +- {pd.Series(correlations.values.flatten()).std().round(3)}, number of valid correlations {sum(number_participants.notna().values.flatten())}"

    return title, fig
