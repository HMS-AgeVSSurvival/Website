from website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import os
import pandas as pd

from website.utils.controls import get_item_radio_items, get_drop_down, get_options_from_dict
from website import METHODS, TARGETS, MAIN_CATEGORIES, CATEGORIES, ALGORITHMS


@APP.callback(
    Output("memory_residual_correlations", "data"),
    [
        Input("method_residual_correlations", "value"),
        Input("target_row_residual_correlations", "value"),
        Input("target_column_residual_correlations", "value"),
    ],
)
def get_residual_correlations(method, target_row, target_column):
    path_to_fetch = f"data/correlation/residual/{method}_{target_row}_{target_column}.feather"
    if os.path.exists(path_to_fetch):
        return pd.read_feather(path_to_fetch).to_dict()
    else:
        return pd.read_feather(f"data/correlation/residual/{method}_{target_column}_{target_row}.feather").T.to_dict()


@APP.callback(
    Output("memory_std_residual_correlations", "data"),
    [
        Input("method_residual_correlations", "value"),
        Input("target_row_residual_correlations", "value"),
        Input("target_column_residual_correlations", "value"),
    ],
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
    [
        Input("target_row_residual_correlations", "value"),
        Input("target_column_residual_correlations", "value"),
    ],
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


def get_controls_axis_residual_correlations(axis):
    return [
        get_item_radio_items(f"target_{axis}_residual_correlations", TARGETS, "Target:"),
        get_item_radio_items(f"main_category_{axis}_residual_correlations", MAIN_CATEGORIES, "Main category:"),
        get_drop_down(f"category_{axis}_residual_correlations", CATEGORIES["examination"], "Category:"),
        get_item_radio_items(f"algorithm_{axis}_residual_correlations", ALGORITHMS, "Algorithm:"),
    ]


@APP.callback(
    [Output("category_row_residual_correlations", "options"), Output("category_row_residual_correlations", "value")],
    Input("main_category_row_residual_correlations", "value"),
)
def update_categories_row(main_category):
    options = get_options_from_dict(CATEGORIES[main_category])

    return options, options[0]["value"]


@APP.callback(
    [
        Output("category_column_residual_correlations", "options"),
        Output("category_column_residual_correlations", "value"),
    ],
    Input("main_category_column_residual_correlations", "value"),
)
def update_categories_column(main_category):
    options = get_options_from_dict(CATEGORIES[main_category])

    return options, options[0]["value"]


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
                dbc.Col(html.H3("Row settings"), width={"size": 2, "offset": 2}),
                dbc.Col(html.H3("Column settings"), width={"size": 2, "offset": 4}),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(dbc.Card(get_controls_axis_residual_correlations("row")), width={"size": 6}),
                dbc.Col(dbc.Card(get_controls_axis_residual_correlations("column")), width={"size": 6}),
            ]
        ),
        dbc.Col(
            [html.H3(id="title_residual_correlations"), dcc.Loading(id="heatmap_residual_correlations")],
            width={"size": 6},
        ),
    ],
    fluid=True,
)
