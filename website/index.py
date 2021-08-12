import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from website.app import APP

import website.introduction as introduction
import website.prediction_performances_residual.page as prediction_performances_residual
import website.prediction_performances_feature_importances.page as prediction_performances_feature_importances

# import website.residual_correlations as residual_correlations


def get_server():
    add_layout(APP)
    return APP.server


def launch_local_website():
    add_layout(APP)
    APP.run_server(debug=True)


def add_layout(app):
    app.layout = html.Div(
        [
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
                    dbc.NavItem(
                        dbc.NavLink(
                            "Prediction performances (residual)",
                            href="/prediction_performances_residual",
                            active=False,
                            id="prediction_performances_residual",
                        )
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            "Prediction performances (feature importances)",
                            href="/prediction_performances_feature_importances",
                            active=False,
                            id="prediction_performances_feature_importances",
                        )
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            "Residual correlations",
                            href="/residual_correlations",
                            active=False,
                            id="residual_correlations",
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


# THIS CALLBACK MAPS THE WEBSITE PAGE ORGANISATION TO THE CODE PAGE ORGANISATION
@APP.callback(Output("page_content", "children"), Input("url", "pathname"))
def _display_page(pathname):
    if "prediction_performances_residual" == pathname.split("/")[1]:
        layout = prediction_performances_residual.LAYOUT

    elif "prediction_performances_feature_importances" == pathname.split("/")[1]:
        layout = prediction_performances_feature_importances.LAYOUT

    elif "residual_correlations" == pathname.split("/")[1]:
        layout = residual_correlations.LAYOUT

    elif "/" == pathname:
        layout = introduction.LAYOUT

    else:
        layout = "404"

    return layout


@APP.callback(
    [
        Output("introduction", "active"),
        Output("prediction_performances_residual", "active"),
        Output("prediction_performances_feature_importances", "active"),
        Output("residual_correlations", "active"),
    ],
    Input("url", "pathname"),
)
def _change_active_page(pathname):
    active_pages = [False] * 4

    if "prediction_performances_residual" == pathname.split("/")[1]:
        active_pages[1] = True

    elif "prediction_performances_feature_importances" == pathname.split("/")[1]:
        active_pages[2] = True

    elif "residual_correlations" == pathname.split("/")[1]:
        active_pages[3] = True

    elif "/" == pathname:
        active_pages[0] = True

    return active_pages
