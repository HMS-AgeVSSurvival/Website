from website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import pandas as pd

from website.utils.controls import get_item_radio_items, get_check_list, get_drop_down
from website.utils.aws_loader import load_feather
from website.feature_importances_correlations.between_algorithms.tabs.shared_plotter import (
    plot_feature_importances_correlations,
)
from website import METHODS, TARGETS, MAIN_CATEGORIES, CATEGORIES, ALGORITHMS, DOWNLOAD_CONFIG


@APP.callback(
    Output("memory_feature_importances_correlations_between_algorithms_all_categories", "data"),
    Input("method_feature_importances_correlations_between_algorithms_all_categories", "value"),
)
def get_residual_correlations_all_categories(method):
    return pd.read_feather(
        f"data/all_categories/correlations/feature_importances/{method}_between_algorithms.feather"
    ).to_dict()


def get_controls_feature_importances_correlations_between_algorithms_all_categories():
    return (
        [
            get_item_radio_items(
                "method_feature_importances_correlations_between_algorithms_all_categories", METHODS, "Method:"
            ),
        ]
        + [
            get_check_list(
                f"targets_feature_importances_correlations_between_algorithms_all_categories",
                TARGETS,
                "Target:",
            )
        ]
        + [
            get_drop_down(
                f"{main_category}_category_feature_importances_correlations_between_algorithms_all_categories",
                CATEGORIES[main_category],
                f"{MAIN_CATEGORIES[main_category]} category:",
                multi=True,
                clearable=True,
                value=["all"] if main_category == "examination" else [],
            )
            for main_category in MAIN_CATEGORIES
        ]
    )


def get_controls_algorithm_feature_importances_correlations_between_algorithms_all_categories(letter):
    algorithms = ALGORITHMS.copy()
    del algorithms["best"]

    return get_item_radio_items(
        f"algorithm_{letter}_feature_importances_correlations_between_algorithms_all_categories",
        algorithms,
        "Algorithm:",
    )


for main_category in MAIN_CATEGORIES:

    @APP.callback(
        Output(
            f"{main_category}_category_feature_importances_correlations_between_algorithms_all_categories",
            "value",
        ),
        Input(
            f"{main_category}_category_feature_importances_correlations_between_algorithms_all_categories",
            "value",
        ),
    )
    def _update_categories_feature_importances_correlations_between_algorithms_all_categories(categories):
        if "all" in categories and len(categories) > 1:  # The last selected category was "all"
            if categories[-1] == "all":
                return ["all"]
            else:
                categories.remove("all")
                return categories
        else:
            raise PreventUpdate


@APP.callback(
    [
        Output("title_feature_importances_correlations_between_algorithms_all_categories", "children"),
        Output("bars_feature_importances_correlations_between_algorithms_all_categories", "figure"),
    ],
    [
        Input("memory_feature_importances_correlations_between_algorithms_all_categories", "data"),
        Input("memory_scores_feature_importances_correlations_between_algorithms_all_categories", "data"),
        Input("memory_information_feature_importances_correlations_between_algorithms_all_categories", "data"),
        Input("targets_feature_importances_correlations_between_algorithms_all_categories", "value"),
    ]
    + [
        Input(f"{main_category}_category_feature_importances_correlations_between_algorithms_all_categories", "value")
        for main_category in MAIN_CATEGORIES
    ]
    + [
        Input(f"algorithm_{letter}_feature_importances_correlations_between_algorithms_all_categories", "value")
        for letter in ["a", "b"]
    ],
)
def _fill_bars_feature_importances_correlations_between_algorithms_all_categories(
    feature_importances_correlations_data,
    scores_data,
    information_data,
    targets,
    examination_categories,
    laboratory_categories,
    questionnaire_categories,
    algorithm_a,
    algorithm_b,
):
    if list(ALGORITHMS.keys()).index(algorithm_a) > list(ALGORITHMS.keys()).index(algorithm_b):
        algorithm_a, algorithm_b = algorithm_b, algorithm_a

    return plot_feature_importances_correlations(
        feature_importances_correlations_data,
        scores_data,
        information_data,
        targets,
        examination_categories,
        laboratory_categories,
        questionnaire_categories,
        algorithm_a,
        algorithm_b,
        custom_categories=False,
    )


def get_all_categories():
    return dbc.Container(
        [
            dcc.Loading(
                [
                    dcc.Store(id="memory_feature_importances_correlations_between_algorithms_all_categories"),
                    dcc.Store(
                        id="memory_scores_feature_importances_correlations_between_algorithms_all_categories",
                        data=load_feather("all_categories/scores_feature_importances.feather").to_dict(),
                    ),
                    dcc.Store(
                        id="memory_information_feature_importances_correlations_between_algorithms_all_categories",
                        data=load_feather("all_categories/information.feather").to_dict(),
                    ),
                ]
            ),
            html.H1("Feature importances correlations"),
            html.Br(),
            html.Br(),
            dbc.Row(
                dbc.Col(
                    dbc.Card(get_controls_feature_importances_correlations_between_algorithms_all_categories()),
                    width={"size": 2, "offset": 5},
                )
            ),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            get_controls_algorithm_feature_importances_correlations_between_algorithms_all_categories(
                                "a"
                            )
                        ),
                        width={"size": 5},
                    ),
                    dbc.Col(dbc.Row(html.H4("VS"), justify="center"), width={"size": 2}),
                    dbc.Col(
                        dbc.Card(
                            get_controls_algorithm_feature_importances_correlations_between_algorithms_all_categories(
                                "b"
                            )
                        ),
                        width={"size": 5},
                    ),
                ]
            ),
            html.Br(),
            html.Br(),
            dbc.Col(
                [
                    dcc.Loading(
                        [
                            html.H3(id="title_feature_importances_correlations_between_algorithms_all_categories"),
                            dcc.Graph(
                                id="bars_feature_importances_correlations_between_algorithms_all_categories",
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
