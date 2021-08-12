from website.app import APP
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from website.residual_correlations.tabs.all_categories import get_all_categories
from website.residual_correlations.tabs.custom_categories import get_custom_categories



@APP.callback(
    Output("tab_content_residual_correlations", "children"),
    Input("tab_manager_residual_correlations", "active_tab"),
)
def _fill_tab(
    active_tab,
):
    if active_tab == "residual_correlations_custom_categories":
        return get_custom_categories()
    else:  # active_tab == "residual_correlations_all_categories":
        return get_all_categories()


LAYOUT = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Custom categories", tab_id="residual_correlations_custom_categories"),
                dbc.Tab(label="All categories", tab_id="residual_correlations_all_categories"),
            ],
            id="tab_manager_residual_correlations",
            active_tab="residual_correlations_custom_categories",
        ),
        html.Div(id="tab_content_residual_correlations"),
    ]
)
