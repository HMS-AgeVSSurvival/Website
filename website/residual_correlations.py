from website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import os
import pandas as pd

from website.utils.controls import get_item_radio_items, get_check_list, get_drop_down, get_options_from_dict
from website import METHODS, TARGETS, MAIN_CATEGORIES, CATEGORIES, ALGORITHMS, AXES


@APP.callback(
    Output("memory_residual_correlations", "data"),
    [
        Input("method_residual_correlations", "value"),
        Input("target_row_residual_correlations", "value"),
        Input("target_column_residual_correlations", "value"),
    ],
)
def get_residual_correlations(method, target_row, target_column):
    path_to_fetch = f"data/correlation/residual/{method}_{target_row}_{target_column}.feather"
    if os.path.exists(path_to_fetch):
        return pd.read_feather(path_to_fetch).to_dict()
    else:
        return pd.read_feather(f"data/correlation/residual/{method}_{target_column}_{target_row}.feather").T.to_dict()


@APP.callback(
    Output("memory_std_residual_correlations", "data"),
    [
        Input("method_residual_correlations", "value"),
        Input("target_row_residual_correlations", "value"),
        Input("target_column_residual_correlations", "value"),
    ],
)
def get_residual_correlations_std(method, target_row, target_column):
    path_to_fetch = f"data/correlation/residual/{method}_std_{target_row}_{target_column}.feather"
    if os.path.exists(path_to_fetch):
        return pd.read_feather(path_to_fetch).to_dict()
    else:
        return pd.read_feather(
            f"data/correlation/residual/{method}_std_{target_column}_{target_row}.feather"
        ).T.to_dict()


@APP.callback(
    Output("memory_number_participants_residual_correlations", "data"),
    [
        Input("target_row_residual_correlations", "value"),
        Input("target_column_residual_correlations", "value"),
    ],
)
def get_residual_correlations_number_partitipants(target_row, target_column):
    path_to_fetch = f"data/correlation/residual/number_participants_{target_row}_{target_column}.feather"
    if os.path.exists(path_to_fetch):
        return pd.read_feather(path_to_fetch).to_dict()
    else:
        return pd.read_feather(
            f"data/correlation/residual/number_participants_{target_column}_{target_row}.feather"
        ).T.to_dict()


def get_controls_residual_correlations():
    return [
        get_item_radio_items("method_residual_correlations", METHODS, "Method:"),
    ]


def get_controls_axis_residual_correlations(key_axis):
    return (
        [get_item_radio_items(f"target_{key_axis}_residual_correlations", TARGETS, "Target:")]
        + [
            get_drop_down(
                f"{main_category}_category_{key_axis}_residual_correlations",
                CATEGORIES[main_category],
                f"{MAIN_CATEGORIES[main_category]} category:",
                multi=True,
                clearable=True,
            )
            for main_category in MAIN_CATEGORIES
        ]
        + [get_check_list(f"algorithm_{axis}_residual_correlations", ALGORITHMS, "Algorithm:")]
    )


for main_category in MAIN_CATEGORIES:
    for axis in AXES:

        @APP.callback(
            Output(f"{main_category}_category_{axis}_residual_correlations", "value"),
            Input(f"{main_category}_category_{axis}_residual_correlations", "value"),
        )
        def update_categories_row(categories):
            if "all" in categories and len(categories) > 1:
                categories.remove("all")
                return categories
            else:
                raise PreventUpdate


@APP.callback(
    [Output("title_residual_correlations", "children"), Output("heatmap_residual_correlations", "figure")],
    [
        Input("memory_residual_correlations", "data"),
        Input("memory_std_residual_correlations", "data"),
        Input("memory_number_participants_residual_correlations", "data"),
    ]
    + [
        Input(f"{main_category}_category_{axis}_residual_correlations", "value")
        for main_category in MAIN_CATEGORIES
        for axis in AXES
    ],
)
def _fill_graph_tab_category(correlations, correlations_std, number_participants, *args):
    (
        examination_categories_row,
        laboratory_categories_row,
        questionnaire_categories_row,
        examination_categories_column,
        laboratory_categories_column,
        questionnaire_categories_column,
    ) = args
    print(
        "examination_categories_row:",
        examination_categories_row,
        "\nlaboratory_categories_row:",
        laboratory_categories_row,
        "\nquestionnaire_categories_row:",
        questionnaire_categories_row,
        "\n\nexamination_categories_column:",
        examination_categories_column,
        "\nlaboratory_categories_column:",
        laboratory_categories_column,
        "\nquestionnaire_categories_column:",
        questionnaire_categories_column,
        "\n\n\n",
    )
    return "Hey", None
    # correlations_raw = pd.DataFrame(data_category).set_index(
    #     ["dimension_1", "subdimension_1", "r2_1", "r2_std_1", "dimension_2", "subdimension_2", "r2_2", "r2_std_2"]
    # )
    # correlations_raw.columns = pd.MultiIndex.from_tuples(
    #     list(map(eval, correlations_raw.columns.tolist())), names=["subset_method", "correlation_type"]
    # )
    # correlations = correlations_raw[[(subset_method, correlation_type), (subset_method, "number_variables")]]
    # correlations.columns = ["correlation", "number_variables"]
    # correlations.reset_index(inplace=True)

    # table_correlations = correlations.pivot(
    #     index=["dimension_1", "subdimension_1"],
    #     columns=["dimension_2", "subdimension_2"],
    #     values="correlation",
    # ).loc[ORDER_DIMENSIONS, ORDER_DIMENSIONS]
    # np.fill_diagonal(table_correlations.values, np.nan)

    # customdata_list = []
    # for customdata_item in ["r2_1", "r2_std_1", "r2_2", "r2_std_2", "number_variables"]:
    #     customdata_list.append(
    #         correlations.pivot(
    #             index=["dimension_1", "subdimension_1"],
    #             columns=["dimension_2", "subdimension_2"],
    #             values=customdata_item,
    #         )
    #         .loc[ORDER_DIMENSIONS, ORDER_DIMENSIONS]
    #         .values
    #     )
    # stacked_customdata = list(map(list, np.dstack(customdata_list)))

    # customdata = pd.DataFrame(None, index=ORDER_DIMENSIONS, columns=ORDER_DIMENSIONS)
    # customdata[customdata.columns] = stacked_customdata

    # hovertemplate = "Correlation: %{z:.3f} <br><br>Dimensions 1: %{x} <br>R²: %{customdata[0]:.3f} +- %{customdata[1]:.3f} <br>Dimensions 2: %{y}<br>R²: %{customdata[2]:.3f} +- %{customdata[3]:.3f} <br>Number variables: %{customdata[4]}<br><extra></extra>"

    # if order_by == "clustering":
    #     fig = heatmap_by_clustering(table_correlations, hovertemplate, customdata)
    # elif order_by == "r2":
    #     sorted_dimensions = (
    #         correlations.set_index(["dimension_1", "subdimension_1"])
    #         .sort_values(by="r2_1", ascending=False)
    #         .index.drop_duplicates()
    #     )

    #     sorted_table_correlations = table_correlations.loc[sorted_dimensions, sorted_dimensions]
    #     sorted_customdata = customdata.loc[sorted_dimensions, sorted_dimensions]

    #     fig = heatmap_by_sorted_dimensions(sorted_table_correlations, hovertemplate, sorted_customdata)

    # else:  # order_by == "custom"
    #     sorted_dimensions = (
    #         correlations.set_index(["dimension_1", "subdimension_1"]).loc[CUSTOM_ORDER].index.drop_duplicates()
    #     )

    #     sorted_table_correlations = table_correlations.loc[sorted_dimensions, sorted_dimensions]
    #     sorted_customdata = customdata.loc[sorted_dimensions, sorted_dimensions]
    #     sorted_table_correlations.index.names = ["dimension", "subdimension"]
    #     fig = heatmap_by_sorted_dimensions(sorted_table_correlations, hovertemplate, sorted_customdata)

    #     fig = add_custom_legend_axis(fig, sorted_table_correlations)

    # fig.update_layout(
    #     yaxis={"showgrid": False, "zeroline": False},
    #     xaxis={"showgrid": False, "zeroline": False},
    #     width=GRAPH_SIZE,
    #     height=GRAPH_SIZE,
    #     margin={"l": 0, "r": 0, "b": 0, "t": 0},
    # )

    # return (
    #     fig,
    #     f"Average correlation = {correlations['correlation'].mean().round(3)} +- {correlations['correlation'].std().round(3)}",
    #     histogram_correlation(table_correlations),
    # )


LAYOUT = dbc.Container(
    [
        dcc.Loading(
            [
                dcc.Store(id="memory_residual_correlations"),
                dcc.Store(id="memory_std_residual_correlations"),
                dcc.Store(id="memory_number_participants_residual_correlations"),
            ]
        ),
        html.H1("Residual correlations"),
        html.Br(),
        html.Br(),
        dbc.Row(dbc.Col(dbc.Card(get_controls_residual_correlations()), width={"size": 2, "offset": 5})),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(html.H3(f"{AXES[list(AXES.keys())[0]]} settings"), width={"size": 2, "offset": 2}),
                dbc.Col(html.H3(f"{AXES[list(AXES.keys())[1]]} settings"), width={"size": 2, "offset": 4}),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(dbc.Card(get_controls_axis_residual_correlations(key_axis)), width={"size": 6})
                for key_axis in AXES
            ]
        ),
        dbc.Col(
            [html.H3(id="title_residual_correlations"), dcc.Loading(id="heatmap_residual_correlations")],
            width={"size": 6},
        ),
    ],
    fluid=True,
)
