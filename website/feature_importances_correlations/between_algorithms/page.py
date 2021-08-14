from website.app import APP
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from website.feature_importances_correlations.between_algorithms.tabs.all_categories import get_all_categories
from website.feature_importances_correlations.between_algorithms.tabs.custom_categories import get_custom_categories


@APP.callback(
    Output("tab_content_feature_importances_correlations_between_algorithms", "children"),
    Input("tab_manager_feature_importances_correlations_between_algorithms", "active_tab"),
)
def _fill_tab(
    active_tab,
):
    if active_tab == "feature_importances_correlations_between_algorithms_custom_categories":
        return get_custom_categories()
    else:  # active_tab == "feature_importances_correlations_between_algorithms_all_categories":
        return get_all_categories()


LAYOUT = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(
                    label="Custom categories",
                    tab_id="feature_importances_correlations_between_algorithms_custom_categories",
                ),
                dbc.Tab(
                    label="All categories", tab_id="feature_importances_correlations_between_algorithms_all_categories"
                ),
            ],
            id="tab_manager_feature_importances_correlations_between_algorithms",
            active_tab="feature_importances_correlations_between_algorithms_custom_categories",
        ),
        html.Div(id="tab_content_feature_importances_correlations_between_algorithms"),
    ]
)
