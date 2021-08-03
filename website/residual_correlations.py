from website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import os
import pandas as pd
import numpy as np

from website.utils.controls import get_item_radio_items, get_check_list, get_drop_down
from website.utils.rename import rename
from website import (
    METHODS,
    TARGETS,
    MAIN_CATEGORIES,
    CATEGORIES,
    ALGORITHMS,
    SCORES,
    AXES,
    AXIS_ROW,
    AXIS_COLUMN,
    GRAPH_SIZE,
    DOWNLOAD_CONFIG,
)


@APP.callback(
    Output("memory_residual_correlations", "data"),
    [Input("method_residual_correlations", "value")]
    + [Input(f"target_{key_axis}_residual_correlations", "value") for key_axis in AXES],
)
def get_residual_correlations(method, target_row, target_column):
    return load_correlations(method, target_row, target_column, std_path="")


@APP.callback(
    Output("memory_std_residual_correlations", "data"),
    [Input("method_residual_correlations", "value")]
    + [Input(f"target_{key_axis}_residual_correlations", "value") for key_axis in AXES],
)
def get_std_residual_correlations(method, target_row, target_column):
    return load_correlations(method, target_row, target_column, std_path="_std")


def load_correlations(method, target_row, target_column, std_path=""):
    path_to_fetch = f"data/correlation/residual/{method}{std_path}_{target_row}_{target_column}.feather"
    if os.path.exists(path_to_fetch):
        return pd.read_feather(path_to_fetch).to_dict()
    else:
        correlations = pd.read_feather(
            f"data/correlation/residual/{method}{std_path}_{target_column}_{target_row}.feather"
        ).set_index(["main_category", "category", "algorithm"])
        correlations.columns = pd.MultiIndex.from_tuples(
            list(map(eval, correlations.columns.tolist())), names=["main_category", "category", "algorithm"]
        )
        correlations_translated = correlations.T
        correlations_translated.columns = map(str, correlations_translated.columns.tolist())

        return correlations_translated.reset_index().to_dict()


@APP.callback(
    Output("memory_number_participants_residual_correlations", "data"),
    [Input(f"target_{key_axis}_residual_correlations", "value") for key_axis in AXES],
)
def get_number_partitipants_residual_correlations(target_row, target_column):
    path_to_fetch = f"data/correlation/residual/number_participants_{target_row}_{target_column}.feather"
    if os.path.exists(path_to_fetch):
        return pd.read_feather(path_to_fetch).to_dict()
    else:
        number_participants = pd.read_feather(
            f"data/correlation/residual/number_participants_{target_column}_{target_row}.feather"
        ).set_index(["main_category", "category"])
        number_participants.columns = pd.MultiIndex.from_tuples(
            list(map(eval, number_participants.columns.tolist())), names=["main_category", "category"]
        )

        number_participants_translated = number_participants.T
        number_participants_translated.columns = map(str, number_participants_translated.columns.tolist())

        return number_participants_translated.reset_index().to_dict()


def get_controls_residual_correlations():
    return [
        get_item_radio_items("method_residual_correlations", METHODS, "Method:"),
    ]


def get_controls_axis_residual_correlations(key_axis):
    return (
        [get_item_radio_items(f"target_{key_axis}_residual_correlations", TARGETS, "Target:")]
        + [
            get_drop_down(
                f"{main_category}_category_{key_axis}_residual_correlations",
                CATEGORIES[main_category],
                f"{MAIN_CATEGORIES[main_category]} category:",
                multi=True,
                clearable=True,
            )
            for main_category in MAIN_CATEGORIES
        ]
        + [get_check_list(f"algorithm_{key_axis}_residual_correlations", ALGORITHMS, "Algorithm:")]
    )


for main_category in MAIN_CATEGORIES:
    for key_axis in AXES:

        @APP.callback(
            Output(f"{main_category}_category_{key_axis}_residual_correlations", "value"),
            Input(f"{main_category}_category_{key_axis}_residual_correlations", "value"),
        )
        def update_categories_row_residual_correlations(categories):
            if "all" in categories and len(categories) > 1:
                categories.remove("all")
                return categories
            else:
                raise PreventUpdate


for key_axis in AXES:

    @APP.callback(
        Output(f"algorithm_{key_axis}_residual_correlations", "value"),
        Input(f"algorithm_{key_axis}_residual_correlations", "value"),
    )
    def update_algorithms_prediction_performances(algorithms):
        if "best" in algorithms and len(algorithms) > 1:
            if algorithms[-1] == "best":  # The last selected algorithm was "best"
                return ["best"]
            else:
                algorithms.remove("best")
                return algorithms
        else:
            raise PreventUpdate


@APP.callback(
    [Output("title_residual_correlations", "children"), Output("heatmap_residual_correlations", "figure")],
    [
        Input("memory_residual_correlations", "data"),
        Input("memory_std_residual_correlations", "data"),
        Input("memory_number_participants_residual_correlations", "data"),
        Input("memory_scores_residual_correlations", "data"),
    ]
    + [
        Input(f"{main_category}_category_{key_axis}_residual_correlations", "value")
        for main_category in MAIN_CATEGORIES
        for key_axis in AXES
    ]
    + [Input(f"algorithm_{key_axis}_residual_correlations", "value") for key_axis in AXES]
    + [Input(f"target_{key_axis}_residual_correlations", "value") for key_axis in AXES],
)
def _fill_heatmap_residual_correlations(
    correlations_data, correlations_std_data, number_participants_data, scores_data, *args
):
    import plotly.graph_objs as go
    from website.utils.graphs import heatmap_by_sorted_index, add_custom_legend_axis

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
    print(args)

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

    metrics = {AXIS_ROW: SCORES[target_row], AXIS_COLUMN: SCORES[target_column]}

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
    scores = pd.DataFrame(scores_data).set_index(["main_category", "category", "algorithm"])
    scores.columns = pd.MultiIndex.from_tuples(
        list(map(eval, scores.columns.tolist())), names=["target", "fold", "metric"]
    )
    scores = scores.loc[correlations.index]  # TO REMOVE

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

    algorithms_to_look_at = {}
    for key_axis in AXES:
        if algorithms[key_axis] == ["best"]:
            algorithms_to_look_at[key_axis] = list(ALGORITHMS.keys())
            algorithms_to_look_at[key_axis].remove("best")
        else:
            algorithms_to_look_at[key_axis] = algorithms[key_axis]

    indexes_to_take = {AXIS_ROW: [], AXIS_COLUMN: []}
    for key_axis in AXES:
        for main_category in MAIN_CATEGORIES:
            if categories_to_display[key_axis][main_category] == ["all"]:
                categories_to_display[key_axis][main_category] = (
                    pd.Index(list(CATEGORIES[main_category].keys())).drop("all").to_list()
                )
            indexes_to_take[key_axis].extend(
                pd.MultiIndex.from_product(
                    ([main_category], categories_to_display[key_axis][main_category], algorithms_to_look_at[key_axis])
                ).to_list()
            )
    indexes = {}
    indexes[AXIS_ROW] = pd.MultiIndex.from_tuples(
        indexes_to_take[AXIS_ROW], names=["main_category", "category", "algorithm"]
    )
    indexes[AXIS_COLUMN] = pd.MultiIndex.from_tuples(
        indexes_to_take[AXIS_COLUMN], names=["main_category", "category", "algorithm"]
    )

    correlations_to_display = correlations.loc[indexes[AXIS_ROW], indexes[AXIS_COLUMN]]
    correlations_std_to_display = correlations_std.loc[indexes[AXIS_ROW], indexes[AXIS_COLUMN]]
    number_participants_to_display = pd.DataFrame(
        None,
        index=pd.MultiIndex.from_tuples(indexes[AXIS_ROW]),
        columns=pd.MultiIndex.from_tuples(indexes[AXIS_COLUMN]),
    )
    number_participants_to_display = number_participants.loc[
        indexes[AXIS_ROW].droplevel("algorithm"),
        indexes[AXIS_COLUMN].droplevel("algorithm"),
    ]
    number_participants_to_display.index = indexes[AXIS_ROW]
    number_participants_to_display.columns = indexes[AXIS_COLUMN]

    scores_template = pd.DataFrame(None, index=indexes[AXIS_ROW], columns=indexes[AXIS_COLUMN])
    scores_to_display = {AXIS_ROW: scores_template.copy(), AXIS_COLUMN: scores_template.copy()}
    scores_std_to_display = {AXIS_ROW: scores_template.copy(), AXIS_COLUMN: scores_template.copy()}

    transposed_template = scores_template.T
    transposed_template[indexes[AXIS_ROW]] = scores.loc[
        indexes[AXIS_ROW], (target[AXIS_ROW], "test", list(metrics[AXIS_ROW].keys())[0])
    ]
    scores_to_display[AXIS_ROW] = transposed_template.T
    transposed_template = scores_template.T
    transposed_template[indexes[AXIS_ROW]] = scores.loc[
        indexes[AXIS_ROW], (target[AXIS_ROW], "test", f"{list(metrics[AXIS_ROW].keys())[0]}_std")
    ]
    scores_std_to_display[AXIS_ROW] = transposed_template.T

    scores_to_display[AXIS_COLUMN][indexes[AXIS_COLUMN]] = scores.loc[
        indexes[AXIS_COLUMN], (target[AXIS_COLUMN], "test", list(metrics[AXIS_COLUMN].keys())[0])
    ]
    scores_std_to_display[AXIS_COLUMN][indexes[AXIS_COLUMN]] = scores.loc[
        indexes[AXIS_COLUMN], (target[AXIS_COLUMN], "test", f"{list(metrics[AXIS_COLUMN].keys())[0]}_std")
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
        stacked_customdata, index=correlations_to_display.index, columns=correlations_to_display.columns
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
                    np.dstack(
                        (
                            [indexes[key_axis].get_level_values("main_category").to_list()],
                            [indexes[key_axis].get_level_values("category").to_list()],
                            [best_algorithms.to_list()],
                        )
                    )[0]
                ),
                names=["main_category", "category", "algorithm"],
            )
        else:
            indexes_algorithms[key_axis] = indexes[key_axis]

    correlations_to_display = correlations_to_display.loc[indexes_algorithms[AXIS_ROW], indexes_algorithms[AXIS_COLUMN]]
    correlations_std_to_display = correlations_std_to_display.loc[
        indexes_algorithms[AXIS_ROW], indexes_algorithms[AXIS_COLUMN]
    ]
    customdata = customdata.loc[indexes_algorithms[AXIS_ROW], indexes_algorithms[AXIS_COLUMN]]

    rename(correlations_to_display)
    rename(correlations_std_to_display)
    rename(customdata)

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


LAYOUT = dbc.Container(
    [
        dcc.Loading(
            [
                dcc.Store(id="memory_residual_correlations"),
                dcc.Store(id="memory_std_residual_correlations"),
                dcc.Store(id="memory_number_participants_residual_correlations"),
                dcc.Store(
                    id="memory_scores_residual_correlations", data=pd.read_feather("data/scores.feather").to_dict()
                ),
            ]
        ),
        html.H1("Residual correlations"),
        html.Br(),
        html.Br(),
        dbc.Row(dbc.Col(dbc.Card(get_controls_residual_correlations()), width={"size": 2, "offset": 5})),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(html.H3(f"{AXES[AXIS_ROW]} settings"), width={"size": 2, "offset": 2}),
                dbc.Col(html.H3(f"{AXES[AXIS_COLUMN]} settings"), width={"size": 2, "offset": 4}),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(dbc.Card(get_controls_axis_residual_correlations(key_axis)), width={"size": 6})
                for key_axis in AXES
            ]
        ),
        dbc.Col(
            [
                dcc.Loading(
                    [
                        html.H3(id="title_residual_correlations"),
                        dcc.Graph(id="heatmap_residual_correlations", config=DOWNLOAD_CONFIG),
                    ]
                )
            ],
            width={"offset": 2},
        ),
    ],
    fluid=True,
)
