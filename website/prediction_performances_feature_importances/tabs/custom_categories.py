from website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import pandas as pd

from website.utils.controls import get_item_radio_items, get_check_list, get_drop_down, get_options_from_dict
from website.prediction_performances_feature_importances.tabs.shared_plotter import plot_scores
from website import TARGETS, MAIN_CATEGORIES, CUSTOM_CATEGORIES, ALGORITHMS, SCORES_FEATURE_IMPORTANCES, DOWNLOAD_CONFIG


def get_controls_prediction_performances_feature_importances_custom_categories():
    return (
        [get_check_list("targets_prediction_performances_feature_importances_custom_categories", TARGETS, "Target:")]
        + [
            get_drop_down(
                f"{main_category}_category_prediction_performances_feature_importances_custom_categories",
                CUSTOM_CATEGORIES[main_category],
                f"{MAIN_CATEGORIES[main_category]} category:",
                multi=True,
                clearable=True,
            )
            for main_category in MAIN_CATEGORIES
        ]
        + [
            get_check_list(
                f"algorithm_prediction_performances_feature_importances_custom_categories", ALGORITHMS, "Algorithm:"
            ),
            get_item_radio_items(
                "metric_prediction_performances_feature_importances_custom_categories",
                SCORES_FEATURE_IMPORTANCES[list(TARGETS.keys())[0]],
                "Target:",
            ),
        ]
    )


for main_category in MAIN_CATEGORIES:

    @APP.callback(
        Output(f"{main_category}_category_prediction_performances_feature_importances_custom_categories", "value"),
        Input(f"{main_category}_category_prediction_performances_feature_importances_custom_categories", "value"),
    )
    def _update_categories_prediction_performances_feature_importances_custom_categories(categories):
        if "all" in categories and len(categories) > 1:  # The last selected category was "all"
            if categories[-1] == "all":
                return ["all"]
            else:
                categories.remove("all")
                return categories
        else:
            raise PreventUpdate


@APP.callback(
    Output("targets_prediction_performances_feature_importances_custom_categories", "value"),
    Input(f"targets_prediction_performances_feature_importances_custom_categories", "value"),
)
def _update_targets_prediction_performances_feature_importances_custom_categories(targets):
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
        Output("metric_prediction_performances_feature_importances_custom_categories", "options"),
        Output("metric_prediction_performances_feature_importances_custom_categories", "value"),
    ],
    Input(f"targets_prediction_performances_feature_importances_custom_categories", "value"),
)
def update_metric_prediction_performances_feature_importances_custom_categories(targets):
    if len(targets) > 0:
        return (
            get_options_from_dict(SCORES_FEATURE_IMPORTANCES[targets[0]]),
            list(SCORES_FEATURE_IMPORTANCES[targets[0]].keys())[0],
        )
    else:
        return (
            get_options_from_dict(SCORES_FEATURE_IMPORTANCES[list(SCORES_FEATURE_IMPORTANCES.keys())[0]]),
            list(SCORES_FEATURE_IMPORTANCES[list(SCORES_FEATURE_IMPORTANCES.keys())[0]].keys())[0],
        )


@APP.callback(
    Output("algorithm_prediction_performances_feature_importances_custom_categories", "value"),
    Input(f"algorithm_prediction_performances_feature_importances_custom_categories", "value"),
)
def update_algorithms_prediction_performances_feature_importances_custom_categories(algorithms):
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
        Output("title_train_prediction_performances_feature_importances_custom_categories", "children"),
        Output("bars_train_prediction_performances_feature_importances_custom_categories", "figure"),
    ],
    [
        Input("memory_prediction_performances_feature_importances_custom_categories", "data"),
        Input("memory_information_prediction_performances_feature_importances_custom_categories", "data"),
        Input("targets_prediction_performances_feature_importances_custom_categories", "value"),
    ]
    + [
        Input(f"{main_category}_category_prediction_performances_feature_importances_custom_categories", "value")
        for main_category in MAIN_CATEGORIES
    ]
    + [
        Input(f"algorithm_prediction_performances_feature_importances_custom_categories", "value"),
        Input(f"metric_prediction_performances_feature_importances_custom_categories", "value"),
    ],
)
def _fill_bars_prediction_performances_feature_importances_custom_categories(
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
        custom_categories=True,
    )


def get_custom_categories():
    return dbc.Container(
        [
            dcc.Loading(
                [
                    dcc.Store(
                        id="memory_prediction_performances_feature_importances_custom_categories",
                        data=pd.read_feather(f"data/custom_categories/scores_feature_importances.feather").to_dict(),
                    ),
                    dcc.Store(
                        id="memory_information_prediction_performances_feature_importances_custom_categories",
                        data=pd.read_feather(f"data/custom_categories/information.feather").to_dict(),
                    ),
                ]
            ),
            html.H1("Prediction performances"),
            html.Br(),
            html.Br(),
            dbc.Row(
                dbc.Col(
                    dbc.Card(get_controls_prediction_performances_feature_importances_custom_categories()),
                    width={"size": 4, "offset": 4},
                )
            ),
            html.Br(),
            html.Br(),
            dbc.Col(
                [
                    dcc.Loading(
                        [
                            html.H3(id="title_train_prediction_performances_feature_importances_custom_categories"),
                            dcc.Graph(
                                id="bars_train_prediction_performances_feature_importances_custom_categories",
                                config=DOWNLOAD_CONFIG,
                            ),
                        ]
                    )
                ],
                width={"offset": 2},
            ),
        ],
        fluid=True,
    )
