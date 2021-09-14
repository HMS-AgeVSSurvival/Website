from website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate


from website.utils.controls import get_check_list, get_drop_down
from website.utils.aws_loader import load_feather
from website.age_residuals_in_survival.tabs.shared_plotter import plot_log_hazard_ratio
from website import MAIN_CATEGORIES, CUSTOM_CATEGORIES, ALGORITHMS, DOWNLOAD_CONFIG


def get_controls_age_residuals_in_survival_custom_categories():
    return [
        get_check_list(
            f"algorithm_age_residuals_in_survival_custom_categories",
            ALGORITHMS,
            "Algorithm used to compute the age residuals:",
        ),
    ] + [
        get_drop_down(
            f"{main_category}_category_age_residuals_in_survival_custom_categories",
            CUSTOM_CATEGORIES[main_category],
            f"{MAIN_CATEGORIES[main_category]} category:",
            multi=True,
            clearable=True,
        )
        for main_category in MAIN_CATEGORIES
    ]


for main_category in MAIN_CATEGORIES:

    @APP.callback(
        Output(f"{main_category}_category_age_residuals_in_survival_custom_categories", "value"),
        Input(f"{main_category}_category_age_residuals_in_survival_custom_categories", "value"),
    )
    def _update_categories_age_residuals_in_survival_custom_categories(categories):
        if "all" in categories and len(categories) > 1:  # The last selected category was "all"
            if categories[-1] == "all":
                return ["all"]
            else:
                categories.remove("all")
                return categories
        else:
            raise PreventUpdate


@APP.callback(
    Output("algorithm_age_residuals_in_survival_custom_categories", "value"),
    Input(f"algorithm_age_residuals_in_survival_custom_categories", "value"),
)
def update_algorithms_age_residuals_in_survival_custom_categories(algorithms):
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
        Output("title_train_age_residuals_in_survival_custom_categories", "children"),
        Output("bars_train_age_residuals_in_survival_custom_categories", "figure"),
    ],
    [
        Input("memory_age_residuals_in_survival_custom_categories", "data"),
        Input("memory_scores_age_residuals_in_survival_custom_categories", "data"),
        Input("memory_information_age_residuals_in_survival_custom_categories", "data"),
    ]
    + [
        Input(f"{main_category}_category_age_residuals_in_survival_custom_categories", "value")
        for main_category in MAIN_CATEGORIES
    ]
    + [Input(f"algorithm_age_residuals_in_survival_custom_categories", "value")],
)
def _fill_bars_age_residuals_in_survival_custom_categories(
    log_hazard_ratio_data,
    scores_data,
    information_data,
    examination_categories,
    laboratory_categories,
    questionnaire_categories,
    algorithms,
):
    return plot_log_hazard_ratio(
        log_hazard_ratio_data,
        scores_data,
        information_data,
        examination_categories,
        laboratory_categories,
        questionnaire_categories,
        algorithms,
        custom_categories=True,
    )


def get_custom_categories():
    return dbc.Container(
        [
            dcc.Loading(
                [
                    dcc.Store(
                        id="memory_age_residuals_in_survival_custom_categories",
                        data=load_feather("custom_categories/log_hazard_ratio.feather").to_dict(),
                    ),
                    dcc.Store(
                        id="memory_scores_age_residuals_in_survival_custom_categories",
                        data=load_feather("custom_categories/scores_residual.feather").to_dict(),
                    ),
                    dcc.Store(
                        id="memory_information_age_residuals_in_survival_custom_categories",
                        data=load_feather("custom_categories/information.feather").to_dict(),
                    ),
                ]
            ),
            html.H1("Age residuals in survival"),
            html.Br(),
            html.Br(),
            dbc.Row(
                dbc.Col(
                    dbc.Card(get_controls_age_residuals_in_survival_custom_categories()),
                    width={"size": 4, "offset": 4},
                )
            ),
            html.Br(),
            html.Br(),
            dbc.Col(
                [
                    dcc.Loading(
                        [
                            html.H3(id="title_train_age_residuals_in_survival_custom_categories"),
                            dcc.Graph(
                                id="bars_train_age_residuals_in_survival_custom_categories",
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
