from website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import pandas as pd

from website.utils.controls import get_item_radio_items, get_check_list, get_drop_down
from website import AGE_SURVIVAL, MAIN_CATEGORIES, CATEGORIES, ALGORITHMS, GRAPH_SIZE, DOWNLOAD_CONFIG


def get_controls_prediction_performances():
    return (
        [get_item_radio_items("target_prediction_performances", AGE_SURVIVAL, "Target:")]
        + [
            get_drop_down(
                f"{main_category}_category_prediction_performances",
                CATEGORIES[main_category],
                f"{MAIN_CATEGORIES[main_category]} category:",
                multi=True,
                clearable=True,
            )
            for main_category in MAIN_CATEGORIES
        ]
        + [get_check_list(f"algorithm_prediction_performances", ALGORITHMS, "Algorithm:")]
    )


for main_category in MAIN_CATEGORIES:

    @APP.callback(
        Output(f"{main_category}_category_prediction_performances", "value"),
        Input(f"{main_category}_category_prediction_performances", "value"),
    )
    def update_categories_row(categories):
        if "all" in categories and len(categories) > 1:
            categories.remove("all")
            return categories
        else:
            raise PreventUpdate


@APP.callback(
    [
        Output("title_test_prediction_performances", "children"),
        Output("bars_test_prediction_performances", "figure"),
        Output("title_train_prediction_performances", "children"),
        Output("bars_train_prediction_performances", "figure"),
    ],
    [Input("memory_prediction_performances", "data"), Input("target_prediction_performances", "value")]
    + [Input(f"{main_category}_category_prediction_performances", "value") for main_category in MAIN_CATEGORIES]
    + [Input(f"algorithm_prediction_performances", "value")],
)
def _fill_bars_prediction_performances(scores_data, target, *args):
    from website.utils.graphs import heatmap_by_sorted_index, add_custom_legend_axis

    return "Hey", None, "Hey", None


LAYOUT = dbc.Container(
    [
        dcc.Loading(
            dcc.Store(id="memory_prediction_performances", data=pd.read_feather(f"data/scores.feather").to_dict())
        ),
        html.H1("Prediction performances"),
        html.Br(),
        html.Br(),
        dbc.Row(dbc.Col(dbc.Card(get_controls_prediction_performances()), width={"size": 4, "offset": 4})),
        html.Br(),
        html.Br(),
        dbc.Col(
            [
                dcc.Loading(
                    [
                        html.H3(id="title_test_prediction_performances"),
                        dcc.Graph(id="bars_test_prediction_performances", config=DOWNLOAD_CONFIG),
                    ]
                )
            ],
            width={"offset": 2},
        ),
        dbc.Col(
            [
                dcc.Loading(
                    [
                        html.H3(id="title_train_prediction_performances"),
                        dcc.Graph(id="bars_train_prediction_performances", config=DOWNLOAD_CONFIG),
                    ]
                )
            ],
            width={"offset": 2},
        ),
    ],
    fluid=True,
)
