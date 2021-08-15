from website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import pandas as pd 

from website.utils.controls import get_item_radio_items, get_check_list, get_drop_down, get_options_from_dict
from website.prediction_performances_residual.tabs.shared_plotter import plot_scores
from website import TARGETS, MAIN_CATEGORIES, CATEGORIES, ALGORITHMS, SCORES_RESIDUAL, DOWNLOAD_CONFIG


def get_controls_prediction_performances_residual_all_categories():
    return (
        [get_check_list("targets_prediction_performances_residual_all_categories", TARGETS, "Target:")]
        + [
            get_drop_down(
                f"{main_category}_category_prediction_performances_residual_all_categories",
                CATEGORIES[main_category],
                f"{MAIN_CATEGORIES[main_category]} category:",
                multi=True,
                clearable=True,
                value=["all"] if main_category == "examination" else [],
            )
            for main_category in MAIN_CATEGORIES
        ]
        + [
            get_check_list(f"algorithm_prediction_performances_residual_all_categories", ALGORITHMS, "Algorithm:"),
            get_item_radio_items(
                "metric_prediction_performances_residual_all_categories",
                SCORES_RESIDUAL[list(TARGETS.keys())[0]],
                "Target:",
            ),
        ]
    )


for main_category in MAIN_CATEGORIES:

    @APP.callback(
        Output(f"{main_category}_category_prediction_performances_residual_all_categories", "value"),
        Input(f"{main_category}_category_prediction_performances_residual_all_categories", "value"),
    )
    def _update_categories_prediction_performances_residual_all_categories(categories):
        if "all" in categories and len(categories) > 1:  # The last selected category was "all"
            if categories[-1] == "all":
                return ["all"]
            else:
                categories.remove("all")
                return categories
        else:
            raise PreventUpdate


@APP.callback(
    Output("targets_prediction_performances_residual_all_categories", "value"),
    Input(f"targets_prediction_performances_residual_all_categories", "value"),
)
def _update_targets_prediction_performances_residual_all_categories(targets):
    if "age" in targets and len(targets) > 1:
        if targets[-1] == "age":  # The last selected target was "age"
            return ["age"]
        else:
            targets.remove("age")
            return targets
    else:
        raise PreventUpdate


@APP.callback(
    [
        Output("metric_prediction_performances_residual_all_categories", "options"),
        Output("metric_prediction_performances_residual_all_categories", "value"),
    ],
    Input(f"targets_prediction_performances_residual_all_categories", "value"),
)
def update_metric_prediction_performances_residual_all_categories(targets):
    if len(targets) > 0:
        return get_options_from_dict(SCORES_RESIDUAL[targets[0]]), list(SCORES_RESIDUAL[targets[0]].keys())[0]
    else:
        return (
            get_options_from_dict(SCORES_RESIDUAL[list(SCORES_RESIDUAL.keys())[0]]),
            list(SCORES_RESIDUAL[list(SCORES_RESIDUAL.keys())[0]].keys())[0],
        )


@APP.callback(
    Output("algorithm_prediction_performances_residual_all_categories", "value"),
    Input(f"algorithm_prediction_performances_residual_all_categories", "value"),
)
def update_algorithms_prediction_performances_residual_all_categories(algorithms):
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
        Output("title_test_prediction_performances_residual_all_categories", "children"),
        Output("bars_test_prediction_performances_residual_all_categories", "figure"),
        Output("title_train_prediction_performances_residual_all_categories", "children"),
        Output("bars_train_prediction_performances_residual_all_categories", "figure"),
    ],
    [
        Input("memory_prediction_performances_residual_all_categories", "data"),
        Input("memory_information_prediction_performances_residual_all_categories", "data"),
        Input("targets_prediction_performances_residual_all_categories", "value"),
    ]
    + [
        Input(f"{main_category}_category_prediction_performances_residual_all_categories", "value")
        for main_category in MAIN_CATEGORIES
    ]
    + [
        Input(f"algorithm_prediction_performances_residual_all_categories", "value"),
        Input(f"metric_prediction_performances_residual_all_categories", "value"),
    ],
)
def _fill_bars_prediction_performances_residual_all_categories(
    scores_data,
    information_data,
    targets,
    examination_categories,
    laboratory_categories,
    questionnaire_categories,
    algorithms,
    metric,
):
    return plot_scores(
        scores_data,
        information_data,
        targets,
        examination_categories,
        laboratory_categories,
        questionnaire_categories,
        algorithms,
        metric,
        custom_categories=False,
    )


def get_all_categories():
    return dbc.Container(
        [
            dcc.Loading(
                [
                    dcc.Store(
                        id="memory_prediction_performances_residual_all_categories",
                        data=pd.read_feather(f"data/all_categories/scores_residual.feather").to_dict(),
                    ),
                    dcc.Store(
                        id="memory_information_prediction_performances_residual_all_categories",
                        data=pd.read_feather(f"data/all_categories/information.feather").to_dict(),
                    ),
                ]
            ),
            html.H1("Prediction performances"),
            html.Br(),
            html.Br(),
            dbc.Row(
                dbc.Col(
                    dbc.Card(get_controls_prediction_performances_residual_all_categories()),
                    width={"size": 4, "offset": 4},
                )
            ),
            html.Br(),
            html.Br(),
            dbc.Col(
                [
                    dcc.Loading(
                        [
                            html.H3(id="title_test_prediction_performances_residual_all_categories"),
                            dcc.Graph(
                                id="bars_test_prediction_performances_residual_all_categories", config=DOWNLOAD_CONFIG
                            ),
                        ]
                    )
                ],
                width={"offset": 2},
            ),
            dbc.Col(
                [
                    dcc.Loading(
                        [
                            html.H3(id="title_train_prediction_performances_residual_all_categories"),
                            dcc.Graph(
                                id="bars_train_prediction_performances_residual_all_categories", config=DOWNLOAD_CONFIG
                            ),
                        ]
                    )
                ],
                width={"offset": 2},
            ),
        ],
        fluid=True,
    )
