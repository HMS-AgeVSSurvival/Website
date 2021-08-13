from website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import os
import pandas as pd

from website.utils.controls import get_item_radio_items, get_check_list, get_drop_down
from website.utils.aws_loader import load_feather
from website.residual_correlations.tabs.share_plotter import plot_heatmap
from website import (
    METHODS,
    TARGETS,
    MAIN_CATEGORIES,
    CATEGORIES,
    ALGORITHMS,
    AXES,
    AXIS_ROW,
    AXIS_COLUMN,
    DOWNLOAD_CONFIG,
)


@APP.callback(
    Output("memory_residual_correlations_all_categories", "data"),
    [Input("method_residual_correlations_all_categories", "value")]
    + [Input(f"target_{key_axis}_residual_correlations_all_categories", "value") for key_axis in AXES],
)
def get_residual_correlations_all_categories(method, target_row, target_column):
    return load_correlations(method, target_row, target_column, std_path="")


@APP.callback(
    Output("memory_std_residual_correlations_all_categories", "data"),
    [Input("method_residual_correlations_all_categories", "value")]
    + [Input(f"target_{key_axis}_residual_correlations_all_categories", "value") for key_axis in AXES],
)
def get_std_residual_correlations_all_categories(method, target_row, target_column):
    return load_correlations(method, target_row, target_column, std_path="_std")


def load_correlations(method, target_row, target_column, std_path=""):
    path_to_fetch = f"all_categories/correlations/residual/{method}{std_path}_{target_row}_{target_column}.feather"
    if os.path.exists(path_to_fetch):
        return load_feather(path_to_fetch).to_dict()
    else:
        correlations = load_feather(
            f"all_categories/correlations/residual/{method}{std_path}_{target_column}_{target_row}.feather"
        ).set_index(["main_category", "category", "algorithm"])
        correlations.columns = pd.MultiIndex.from_tuples(
            list(map(eval, correlations.columns.tolist())), names=["main_category", "category", "algorithm"]
        )
        correlations_translated = correlations.T
        correlations_translated.columns = map(str, correlations_translated.columns.tolist())

        return correlations_translated.reset_index().to_dict()


@APP.callback(
    Output("memory_number_participants_residual_correlations_all_categories", "data"),
    [Input(f"target_{key_axis}_residual_correlations_all_categories", "value") for key_axis in AXES],
)
def get_number_partitipants_residual_correlations_all_categories(target_row, target_column):
    path_to_fetch = f"all_categories/correlations/residual/number_participants_{target_row}_{target_column}.feather"
    if os.path.exists(path_to_fetch):
        return load_feather(path_to_fetch).to_dict()
    else:
        number_participants = load_feather(
            f"all_categories/correlations/residual/number_participants_{target_column}_{target_row}.feather"
        ).set_index(["main_category", "category"])
        number_participants.columns = pd.MultiIndex.from_tuples(
            list(map(eval, number_participants.columns.tolist())), names=["main_category", "category"]
        )

        number_participants_translated = number_participants.T
        number_participants_translated.columns = map(str, number_participants_translated.columns.tolist())

        return number_participants_translated.reset_index().to_dict()


def get_controls_residual_correlations_all_categories():
    return [
        get_item_radio_items("method_residual_correlations_all_categories", METHODS, "Method:"),
    ]


def get_controls_axis_residual_correlations_all_categories(key_axis):
    return (
        [get_item_radio_items(f"target_{key_axis}_residual_correlations_all_categories", TARGETS, "Target:")]
        + [
            get_drop_down(
                f"{main_category}_category_{key_axis}_residual_correlations_all_categories",
                CATEGORIES[main_category],
                f"{MAIN_CATEGORIES[main_category]} category:",
                multi=True,
                clearable=True,
                value=["all"] if main_category == "examination" else [],
            )
            for main_category in MAIN_CATEGORIES
        ]
        + [get_check_list(f"algorithm_{key_axis}_residual_correlations_all_categories", ALGORITHMS, "Algorithm:")]
    )


for main_category in MAIN_CATEGORIES:
    for key_axis in AXES:

        @APP.callback(
            Output(f"{main_category}_category_{key_axis}_residual_correlations_all_categories", "value"),
            Input(f"{main_category}_category_{key_axis}_residual_correlations_all_categories", "value"),
        )
        def _update_categories_row_residual_correlations_all_categories(categories):
            if "all" in categories and len(categories) > 1:  # The last selected category was "all"
                if categories[-1] == "all":
                    return ["all"]
                else:
                    categories.remove("all")
                    return categories
            else:
                raise PreventUpdate


for key_axis in AXES:

    @APP.callback(
        Output(f"algorithm_{key_axis}_residual_correlations_all_categories", "value"),
        Input(f"algorithm_{key_axis}_residual_correlations_all_categories", "value"),
    )
    def _update_algorithms_prediction_performances(algorithms):
        if "best" in algorithms and len(algorithms) > 1:
            if algorithms[-1] == "best":  # The last selected algorithm was "best"
                return ["best"]
            else:
                algorithms.remove("best")
                return algorithms
        else:
            raise PreventUpdate


@APP.callback(
    [
        Output("title_residual_correlations_all_categories", "children"),
        Output("heatmap_residual_correlations_all_categories", "figure"),
    ],
    [
        Input("memory_residual_correlations_all_categories", "data"),
        Input("memory_std_residual_correlations_all_categories", "data"),
        Input("memory_number_participants_residual_correlations_all_categories", "data"),
        Input("memory_scores_residual_correlations_all_categories", "data"),
    ]
    + [
        Input(f"{main_category}_category_{key_axis}_residual_correlations_all_categories", "value")
        for main_category in MAIN_CATEGORIES
        for key_axis in AXES
    ]
    + [Input(f"algorithm_{key_axis}_residual_correlations_all_categories", "value") for key_axis in AXES]
    + [Input(f"target_{key_axis}_residual_correlations_all_categories", "value") for key_axis in AXES],
)
def _fill_heatmap_residual_correlations_all_categories(
    correlations_data, correlations_std_data, number_participants_data, scores_data, *args
):
    return plot_heatmap(
        correlations_data, correlations_std_data, number_participants_data, scores_data, *args, custom_categories=False
    )


def get_all_categories():
    return dbc.Container(
        [
            dcc.Loading(
                [
                    dcc.Store(id="memory_residual_correlations_all_categories"),
                    dcc.Store(id="memory_std_residual_correlations_all_categories"),
                    dcc.Store(id="memory_number_participants_residual_correlations_all_categories"),
                    dcc.Store(
                        id="memory_scores_residual_correlations_all_categories",
                        data=load_feather("all_categories/scores_residual.feather").to_dict(),
                    ),
                ]
            ),
            html.H1("Residual correlations"),
            html.Br(),
            html.Br(),
            dbc.Row(
                dbc.Col(dbc.Card(get_controls_residual_correlations_all_categories()), width={"size": 2, "offset": 5})
            ),
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
                    dbc.Col(
                        dbc.Card(get_controls_axis_residual_correlations_all_categories(key_axis)), width={"size": 6}
                    )
                    for key_axis in AXES
                ]
            ),
            dbc.Col(
                [
                    dcc.Loading(
                        [
                            html.H3(id="title_residual_correlations_all_categories"),
                            dcc.Graph(id="heatmap_residual_correlations_all_categories", config=DOWNLOAD_CONFIG),
                        ]
                    )
                ],
                width={"offset": 2},
            ),
        ],
        fluid=True,
    )
