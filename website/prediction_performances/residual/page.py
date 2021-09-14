from website.app import APP
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from website.prediction_performances.residual.tabs.all_categories import get_all_categories
from website.prediction_performances.residual.tabs.custom_categories import get_custom_categories


@APP.callback(
    Output("tab_content_prediction_performances_residual", "children"),
    Input("tab_manager_prediction_performances_residual", "active_tab"),
)
def _fill_tab(
    active_tab,
):
    if active_tab == "prediction_performances_residual_custom_categories":
        return get_custom_categories()
    else:  # active_tab == "prediction_performances_residual_all_categories":
        return get_all_categories()


LAYOUT = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Custom categories", tab_id="prediction_performances_residual_custom_categories"),
                dbc.Tab(label="All categories", tab_id="prediction_performances_residual_all_categories"),
            ],
            id="tab_manager_prediction_performances_residual",
            active_tab="prediction_performances_residual_custom_categories",
        ),
        html.Div(id="tab_content_prediction_performances_residual"),
    ]
)
