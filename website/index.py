import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from website.app import APP

import website.introduction as introduction

import website.prediction_performances.residual.page as prediction_performances_residual
import website.prediction_performances.feature_importances.page as prediction_performances_feature_importances

import website.residual_correlations.page as residual_correlations

import website.feature_importances_correlations.between_targets.page as feature_importances_correlations_between_targets
import website.feature_importances_correlations.between_algorithms.page as feature_importances_correlations_between_algorithms

import website.feature_importances.page as feature_importances

import website.age_residuals_in_survival.page as age_residuals_in_survival

import website.dataset.page as dataset


def get_server():
    add_layout(APP)
    return APP.server


def launch_local_website():
    add_layout(APP)
    APP.run_server(debug=True)


def add_layout(app):
    app.layout = html.Div(
        [
            html.Div(id="blank-output"),
            dcc.Location(id="url", refresh=False),
            get_top_bar(),
            html.Hr(),
            html.Div(id="page_content"),
        ],
        style={"height": "100vh", "fontSize": 14},
    )


def get_top_bar():
    return html.Div(
        [
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Introduction", href="/", active=False, id="introduction")),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem(
                                "Residual",
                                href="/prediction_performances/residual",
                                id="prediction_performances_residual",
                            ),
                            dbc.DropdownMenuItem(
                                "Feature importances (supplementary)",
                                href="/prediction_performances/feature_importances",
                                id="prediction_performances_feature_importances",
                            ),
                        ],
                        label="Prediction performances",
                        nav=True,
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            "Residual correlations",
                            href="/residual_correlations",
                            active=False,
                            id="residual_correlations",
                        )
                    ),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem(
                                "Between targets",
                                href="/feature_importances_correlations/between_targets",
                                id="feature_importances_correlations_between_targets",
                            ),
                            dbc.DropdownMenuItem(
                                "Between algorithms",
                                href="/feature_importances_correlations/between_algorithms",
                                id="feature_importances_correlations_between_algorithms",
                            ),
                        ],
                        label="Feature importances correlations",
                        nav=True,
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            "Feature importances",
                            href="/feature_importances",
                            active=False,
                            id="feature_importances",
                        )
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            "Age residuals in survival",
                            href="/age_residuals_in_survival",
                            active=False,
                            id="age_residuals_in_survival",
                        )
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            "Dataset",
                            href="/dataset",
                            active=False,
                            id="dataset",
                        )
                    ),
                ],
                fill=True,
                pills=True,
            ),
        ],
        style={
            "top": 0,
            "left": 50,
            "bottom": 0,
            "right": 50,
            "padding": "1rem 1rem",
        },
    )


@APP.callback(Output("page_content", "children"), Input("url", "pathname"))
def _display_page(pathname):
    layout = "404"

    if "prediction_performances" == pathname.split("/")[1]:
        if "residual" == pathname.split("/")[2]:
            layout = prediction_performances_residual.LAYOUT
        elif "feature_importances" == pathname.split("/")[2]:
            layout = prediction_performances_feature_importances.LAYOUT

    elif "residual_correlations" == pathname.split("/")[1]:
        layout = residual_correlations.LAYOUT

    elif "feature_importances_correlations" == pathname.split("/")[1]:
        if "between_targets" == pathname.split("/")[2]:
            layout = feature_importances_correlations_between_targets.LAYOUT
        elif "between_algorithms" == pathname.split("/")[2]:
            layout = feature_importances_correlations_between_algorithms.LAYOUT

    elif "feature_importances" == pathname.split("/")[1]:
        layout = feature_importances.LAYOUT

    elif "age_residuals_in_survival" == pathname.split("/")[1]:
        layout = age_residuals_in_survival.LAYOUT

    elif "dataset" == pathname.split("/")[1]:
        layout = dataset.LAYOUT

    elif "/" == pathname:
        layout = introduction.LAYOUT

    return layout


APP.clientside_callback(
    """
    function(pathname) {
        document.title = "Page not found on Age VS Survival"
        if ("prediction_performances" === pathname.split("/")[1]) {
            if ("residual" === pathname.split("/")[2]) {
                document.title = "Prediction performances - Residual"
            } else if ("feature_importances" === pathname.split("/")[2]) {
                document.title = "Prediction performances - Feature importances"
            }
        } else if ("residual_correlations" === pathname.split("/")[1]) {
            document.title = "Residual correlations"
        } else if ("feature_importances_correlations" === pathname.split("/")[1]) {
            if ("between_targets" === pathname.split("/")[2]) {
                document.title = "Feature importances correlations - Between targets"
            } else if ("between_algorithms" === pathname.split("/")[2]) {
                document.title = "Feature importances correlations - Between algorithms"
            }
        } else if ("feature_importances" === pathname.split("/")[1]) {
            document.title = "Feature importances"
        } else if ("age_residuals_in_survival" === pathname.split("/")[1]) {
            document.title = "Age residuals in survival"
        } else if ("dataset" === pathname.split("/")[1]) {
            document.title = "Dataset"
        } else if ("/" === pathname) {
            document.title = "Age VS Survival"
        }
    }
    """,
    Output("blank-output", "children"),
    Input("url", "pathname"),
)


@APP.callback(
    [
        Output("introduction", "active"),
        Output("prediction_performances_residual", "active"),
        Output("prediction_performances_feature_importances", "active"),
        Output("residual_correlations", "active"),
        Output("feature_importances_correlations_between_targets", "active"),
        Output("feature_importances_correlations_between_algorithms", "active"),
        Output("feature_importances", "active"),
        Output("age_residuals_in_survival", "active"),
        Output("dataset", "active"),
    ],
    Input("url", "pathname"),
)
def _change_active_page(pathname):
    active_pages = [False] * 9

    if "prediction_performances" == pathname.split("/")[1]:
        if "residual" == pathname.split("/")[1]:
            active_pages[1] = True
        elif "feature_importances" == pathname.split("/")[2]:
            active_pages[2] = True

    elif "residual_correlations" == pathname.split("/")[1]:
        active_pages[3] = True

    elif "feature_importances_correlations" == pathname.split("/")[1]:
        if "between_targets" == pathname.split("/")[2]:
            active_pages[4] = True
        elif "between_algorithms" == pathname.split("/")[2]:
            active_pages[5] = True

    elif "feature_importances" == pathname.split("/")[1]:
        active_pages[6] = True

    elif "age_residuals_in_survival" == pathname.split("/")[1]:
        active_pages[7] = True

    elif "dataset" == pathname.split("/")[1]:
        active_pages[8] = True

    elif "/" == pathname:
        active_pages[0] = True

    return active_pages
