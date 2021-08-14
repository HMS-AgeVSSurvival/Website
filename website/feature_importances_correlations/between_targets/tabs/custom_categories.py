from website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import pandas as pd

from website.utils.controls import get_item_radio_items, get_check_list, get_drop_down
from website.feature_importances_correlations.between_targets.tabs.shared_plotter import plot_correlations
from website import METHODS, TARGETS, MAIN_CATEGORIES, CUSTOM_CATEGORIES, ALGORITHMS, DOWNLOAD_CONFIG


def get_controls_target_feature_importances_correlations_between_targets_custom_categories(number):
    return get_item_radio_items(
        f"target_{number}_feature_importances_correlations_between_targets_custom_categories",
        TARGETS,
        "Target:",
    )


def get_controls_feature_importances_correlations_between_targets_custom_categories():
    return (
        [
            get_item_radio_items(
                "method_feature_importances_correlations_between_targets_custom_categories", METHODS, "Method:"
            ),
        ]
        + [
            get_drop_down(
                f"{main_category}_category_feature_importances_correlations_between_targets_custom_categories",
                CUSTOM_CATEGORIES[main_category],
                f"{MAIN_CATEGORIES[main_category]} category:",
                multi=True,
                clearable=True,
            )
            for main_category in MAIN_CATEGORIES
        ]
        + [
            get_check_list(
                f"algorithm_feature_importances_correlations_between_targets_custom_categories",
                ALGORITHMS,
                "Algorithm:",
            )
        ]
    )


for main_category in MAIN_CATEGORIES:

    @APP.callback(
        Output(
            f"{main_category}_category_feature_importances_correlations_between_targets_custom_categories",
            "value",
        ),
        Input(
            f"{main_category}_category_feature_importances_correlations_between_targets_custom_categories",
            "value",
        ),
    )
    def _update_categories_feature_importances_correlations_between_targets_custom_categories(categories):
        if "all" in categories and len(categories) > 1:  # The last selected category was "all"
            if categories[-1] == "all":
                return ["all"]
            else:
                categories.remove("all")
                return categories
        else:
            raise PreventUpdate


@APP.callback(
    Output(f"algorithm_feature_importances_correlations_between_targets_custom_categories", "value"),
    Input(f"algorithm_feature_importances_correlations_between_targets_custom_categories", "value"),
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


# @APP.callback(
#     [
#         Output("title_train_prediction_performances_feature_importances_custom_categories", "children"),
#         Output("bars_train_prediction_performances_feature_importances_custom_categories", "figure"),
#     ],
#     [
#         Input("memory_prediction_performances_feature_importances_custom_categories", "data"),
#         Input("memory_information_prediction_performances_feature_importances_custom_categories", "data"),
#         Input("targets_prediction_performances_feature_importances_custom_categories", "value"),
#     ]
#     + [
#         Input(f"{main_category}_category_prediction_performances_feature_importances_custom_categories", "value")
#         for main_category in MAIN_CATEGORIES
#     ]
#     + [
#         Input(f"algorithm_prediction_performances_feature_importances_custom_categories", "value"),
#         Input(f"metric_prediction_performances_feature_importances_custom_categories", "value"),
#     ],
# )
def _fill_bars_prediction_performances_feature_importances_custom_categories(
    correlations_data,
    scores_data,
    information_data,
    target_a,
    target_b,
    examination_categories,
    laboratory_categories,
    questionnaire_categories,
    algorithms,
    metric,
):
    if TARGETS.index(target_a) > TARGETS.index(target_b):
        target_a, target_b = target_b, target_a

    return plot_correlations(
        correlations_data,
        scores_data,
        information_data,
        target_a,
        target_b,
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
                    dcc.Store(id="memory_feature_importances_correlations_between_targets_custom_categories"),
                    dcc.Store(
                        id="memory_scores_feature_importances_correlations_between_targets_custom_categories",
                        data=pd.read_feather("data/custom_categories/scores_residual.feather").to_dict(),
                    ),
                    dcc.Store(
                        id="memory_information_feature_importances_correlations_between_targets_custom_categories",
                        data=pd.read_feather("data/custom_categories/information.feather").to_dict(),
                    ),
                ]
            ),
            html.H1("Feature importances correlations"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            get_controls_target_feature_importances_correlations_between_targets_custom_categories(1)
                        ),
                        width={"size": 5},
                    ),
                    dbc.Col(dbc.Row(html.H4("VS"), justify="center"), width={"size": 2}),
                    dbc.Col(
                        dbc.Card(
                            get_controls_target_feature_importances_correlations_between_targets_custom_categories(2)
                        ),
                        width={"size": 5},
                    ),
                ]
            ),
            html.Br(),
            html.Br(),
            dbc.Row(
                dbc.Col(
                    dbc.Card(get_controls_feature_importances_correlations_between_targets_custom_categories()),
                    width={"size": 2, "offset": 5},
                )
            ),
            html.Br(),
            html.Br(),
            dbc.Col(
                [
                    dcc.Loading(
                        [
                            html.H3(id="title_feature_importances_correlations_between_targets_custom_categories"),
                            dcc.Graph(
                                id="heatmap_feature_importances_correlations_between_targets_custom_categories",
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
