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
from website import (
    METHODS,
    TARGETS,
    MAIN_CATEGORIES,
    CATEGORIES,
    ALGORITHMS,
    AXES,
    AXIS_ROW,
    AXIS_COLUMN,
    GRAPH_SIZE,
    DOWNLOAD_CONFIG,
)


@APP.callback(
    Output("memory_residual_correlations", "data"),
    [Input("method_residual_correlations", "value")]
    + [Input(f"target_{axis}_residual_correlations", "value") for axis in AXES],
)
def get_residual_correlations(method, target_row, target_column):
    path_to_fetch = f"data/correlation/residual/{method}_{target_row}_{target_column}.feather"
    if os.path.exists(path_to_fetch):
        return pd.read_feather(path_to_fetch).to_dict()
    else:
        return pd.read_feather(f"data/correlation/residual/{method}_{target_column}_{target_row}.feather").T.to_dict()


@APP.callback(
    Output("memory_std_residual_correlations", "data"),
    [Input("method_residual_correlations", "value")]
    + [Input(f"target_{axis}_residual_correlations", "value") for axis in AXES],
)
def get_residual_correlations_std(method, target_row, target_column):
    path_to_fetch = f"data/correlation/residual/{method}_std_{target_row}_{target_column}.feather"
    if os.path.exists(path_to_fetch):
        return pd.read_feather(path_to_fetch).to_dict()
    else:
        return pd.read_feather(
            f"data/correlation/residual/{method}_std_{target_column}_{target_row}.feather"
        ).T.to_dict()


@APP.callback(
    Output("memory_number_participants_residual_correlations", "data"),
    [Input(f"target_{axis}_residual_correlations", "value") for axis in AXES],
)
def get_residual_correlations_number_partitipants(target_row, target_column):
    path_to_fetch = f"data/correlation/residual/number_participants_{target_row}_{target_column}.feather"
    if os.path.exists(path_to_fetch):
        return pd.read_feather(path_to_fetch).to_dict()
    else:
        return pd.read_feather(
            f"data/correlation/residual/number_participants_{target_column}_{target_row}.feather"
        ).T.to_dict()


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
    for axis in AXES:

        @APP.callback(
            Output(f"{main_category}_category_{axis}_residual_correlations", "value"),
            Input(f"{main_category}_category_{axis}_residual_correlations", "value"),
        )
        def update_categories_row(categories):
            if "all" in categories and len(categories) > 1:
                categories.remove("all")
                return categories
            else:
                raise PreventUpdate


@APP.callback(
    [Output("title_residual_correlations", "children"), Output("heatmap_residual_correlations", "figure")],
    [
        Input("memory_residual_correlations", "data"),
        Input("memory_std_residual_correlations", "data"),
        Input("memory_number_participants_residual_correlations", "data"),
    ]
    + [
        Input(f"{main_category}_category_{axis}_residual_correlations", "value")
        for main_category in MAIN_CATEGORIES
        for axis in AXES
    ]
    + [Input(f"algorithm_{axis}_residual_correlations", "value") for axis in AXES],
)
def _fill_heatmap_residual_correlations(correlations_data, correlations_std_data, number_participants_data, *args):
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
    ) = args

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
    hovertemplate = (
        "Correlation: %{z:.3f} +- %{customdata[0]:.3f} <br>"
        + list(AXES.values())[0]
        + ": %{y} <br>"
        + list(AXES.values())[1]
        + ": %{x} <br>%{customdata[1]} participants<br><extra></extra>"
    )

    indexes_to_take = {AXIS_ROW: [], AXIS_COLUMN: []}
    indexes_to_rename = {}

    for axis in AXES:
        for main_category in MAIN_CATEGORIES:
            indexes_to_rename[main_category] = MAIN_CATEGORIES[main_category]
            if categories_to_display[axis][main_category] == ["all"]:
                categories_to_display[axis][main_category] = (
                    pd.Index(list(CATEGORIES[main_category].keys())).drop("all").to_list()
                )
            for category in categories_to_display[axis][main_category]:
                indexes_to_rename[category] = CATEGORIES[main_category][category]
                for algorithm in algorithms[axis]:
                    indexes_to_rename[algorithm] = ALGORITHMS[algorithm]
                    indexes_to_take[axis].append([main_category, category, algorithm])

    correlations_to_display = correlations.loc[indexes_to_take[AXIS_ROW], indexes_to_take[AXIS_COLUMN]]
    correlations_std_to_display = correlations_std.loc[indexes_to_take[AXIS_ROW], indexes_to_take[AXIS_COLUMN]]
    number_participants_to_display = pd.DataFrame(
        None,
        index=pd.MultiIndex.from_tuples(indexes_to_take[AXIS_ROW]),
        columns=pd.MultiIndex.from_tuples(indexes_to_take[AXIS_COLUMN]),
    )
    number_participants_to_display[number_participants_to_display.columns] = number_participants.loc[
        pd.MultiIndex.from_tuples(map(lambda line: line[:2], indexes_to_take[AXIS_ROW])),
        pd.MultiIndex.from_tuples(map(lambda line: line[:2], indexes_to_take[AXIS_COLUMN])),
    ].values

    customdata_list = [correlations_std_to_display, number_participants_to_display]
    stacked_customdata = list(map(list, np.dstack(customdata_list)))
    customdata = pd.DataFrame(
        stacked_customdata, index=correlations_to_display.index, columns=correlations_to_display.columns
    )

    correlations_to_display.rename(index=indexes_to_rename, columns=indexes_to_rename, inplace=True)
    correlations_std_to_display.rename(index=indexes_to_rename, columns=indexes_to_rename, inplace=True)
    customdata.rename(index=indexes_to_rename, columns=indexes_to_rename, inplace=True)

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

    return (
        f"Average correlation = {correlations_to_display.mean().mean().round(3)} +- {pd.Series(correlations_to_display.values.flatten()).std().round(3)}, number of valid correlations {number_participants_to_display.notna().sum().sum()}",
        fig,
    )


LAYOUT = dbc.Container(
    [
        dcc.Loading(
            [
                dcc.Store(id="memory_residual_correlations"),
                dcc.Store(id="memory_std_residual_correlations"),
                dcc.Store(id="memory_number_participants_residual_correlations"),
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
