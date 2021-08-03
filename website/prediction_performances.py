from website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import pandas as pd
import numpy as np

from website.utils.controls import get_item_radio_items, get_check_list, get_drop_down, get_options_from_dict
from website.utils.rename import rename
from website import TARGETS, MAIN_CATEGORIES, CATEGORIES, ALGORITHMS, FOLDS, SCORES, GRAPH_SIZE, DOWNLOAD_CONFIG


def get_controls_prediction_performances():
    return (
        [get_check_list("targets_prediction_performances", TARGETS, "Target:")]
        + [
            get_drop_down(
                f"{main_category}_category_prediction_performances",
                CATEGORIES[main_category],
                f"{MAIN_CATEGORIES[main_category]} category:",
                multi=True,
                clearable=True,
            )
            for main_category in MAIN_CATEGORIES
        ]
        + [
            get_check_list(f"algorithm_prediction_performances", ALGORITHMS, "Algorithm:"),
            get_item_radio_items("metric_prediction_performances", SCORES[list(TARGETS.keys())[0]], "Target:"),
        ]
    )


for main_category in MAIN_CATEGORIES:

    @APP.callback(
        Output(f"{main_category}_category_prediction_performances", "value"),
        Input(f"{main_category}_category_prediction_performances", "value"),
    )
    def update_categories_prediction_performances(categories):
        if "all" in categories and len(categories) > 1:
            categories.remove("all")
            return categories
        else:
            raise PreventUpdate


@APP.callback(
    Output("targets_prediction_performances", "value"),
    Input(f"targets_prediction_performances", "value"),
)
def update_targets_prediction_performances(targets):
    if "age" in targets and len(targets) > 1:
        if targets[-1] == "age":  # The last selected target was "age"
            return ["age"]
        else:
            targets.remove("age")
            return targets
    else:
        raise PreventUpdate


@APP.callback(
    [Output("metric_prediction_performances", "options"), Output("metric_prediction_performances", "value")],
    Input(f"targets_prediction_performances", "value"),
)
def update_metric_prediction_performances(targets):
    if len(targets) > 0:
        return get_options_from_dict(SCORES[targets[0]]), list(SCORES[targets[0]].keys())[0]
    else:
        return get_options_from_dict(SCORES[list(SCORES.keys())[0]]), list(SCORES[list(SCORES.keys())[0]].keys())[0]


@APP.callback(
    Output("algorithm_prediction_performances", "value"), Input(f"algorithm_prediction_performances", "value")
)
def update_algorithms_prediction_performances(algorithms):
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
        Output("title_test_prediction_performances", "children"),
        Output("bars_test_prediction_performances", "figure"),
        Output("title_train_prediction_performances", "children"),
        Output("bars_train_prediction_performances", "figure"),
    ],
    [
        Input("memory_prediction_performances", "data"),
        Input("memory_information_prediction_performances", "data"),
        Input("targets_prediction_performances", "value"),
    ]
    + [Input(f"{main_category}_category_prediction_performances", "value") for main_category in MAIN_CATEGORIES]
    + [Input(f"algorithm_prediction_performances", "value"), Input(f"metric_prediction_performances", "value")],
)
def _fill_bars_prediction_performances(
    scores_data,
    information_data,
    targets,
    examination_categories,
    laboratory_categories,
    questionnaire_categories,
    algorithms,
    metric,
):
    import plotly.graph_objs as go
    from website.utils.graphs import add_custom_legend_axis

    if len(targets) == 0:
        return "Please select a target", go.Figure(), "", go.Figure()
    elif len(examination_categories) + len(laboratory_categories) + len(questionnaire_categories) == 0:
        return "Please select a category", go.Figure(), "", go.Figure()
    elif len(algorithms) == 0:
        return "Please select an algorithm", go.Figure(), "", go.Figure()

    scores_full = pd.DataFrame(scores_data).set_index(["main_category", "category", "algorithm"])
    scores_full.columns = pd.MultiIndex.from_tuples(
        list(map(eval, scores_full.columns.tolist())), names=["target", "fold", "metric"]
    )
    information_full = pd.DataFrame(information_data).set_index(["main_category", "category"])
    information_full.columns = pd.MultiIndex.from_tuples(
        list(map(eval, information_full.columns.tolist())), names=["target", "information", "detail"]
    )

    categories_to_display = {
        "examination": examination_categories,
        "laboratory": laboratory_categories,
        "questionnaire": questionnaire_categories,
    }

    if algorithms == ["best"]:
        algorithms_to_look_at = list(ALGORITHMS.keys())
        algorithms_to_look_at.remove("best")
    else:
        algorithms_to_look_at = algorithms

    list_indexes_to_take = []
    for main_category in MAIN_CATEGORIES:
        if categories_to_display[main_category] == ["all"]:
            categories_to_display[main_category] = (
                pd.Index(list(CATEGORIES[main_category].keys())).drop("all").to_list()
            )
        list_indexes_to_take.extend(
            pd.MultiIndex.from_product(
                ([main_category], categories_to_display[main_category], algorithms_to_look_at)
            ).to_list()
        )
    indexes_to_take = pd.MultiIndex.from_tuples(list_indexes_to_take, names=["main_category", "category", "algorithm"])
    scores = scores_full.loc[indexes_to_take, (targets, list(FOLDS.keys()), [metric, f"{metric}_std"])]
    information = information_full.loc[indexes_to_take.droplevel("algorithm").drop_duplicates(), targets]

    rename(scores, columns=False)
    rename(information, algorithm=False, columns=False)

    indexes_target_best_algorithms = {}
    if algorithms == ["best"]:
        scores_grouped_by_categories = scores.reset_index().groupby(by=["main_category", "category"])

        for target in targets:
            best_algorithms = list(
                map(
                    lambda group: group[1].set_index("algorithm")[(target, "test", metric)].idxmax(),
                    scores_grouped_by_categories,
                )
            )
            best_algorithms = pd.Series(best_algorithms).replace(np.nan, ALGORITHMS[algorithms_to_look_at[0]])
            indexes_target_best_algorithms[target] = pd.MultiIndex.from_tuples(
                list(
                    np.dstack(
                        (
                            [information.index.get_level_values("main_category").to_list()],
                            [information.index.get_level_values("category").to_list()],
                            [best_algorithms.to_list()],
                        )
                    )[0]
                ),
                names=["main_category", "category", "algorithm"],
            )

    if targets != ["age"]:
        scores.replace(-1, np.nan, inplace=True)
    hovertemplate = "%{x},<Br> score: %{y:.3f} +- %{customdata[0]:.3f}, %{customdata[1]} participants with %{customdata[2]} variables, age range %{customdata[3]} to %{customdata[4]} years old <extra>%{customdata[5]}</extra>"

    figures = {}
    titles = {}

    for fold in FOLDS:
        scores_fold = scores.loc[:, (slice(None), fold)]

        if sum(scores_fold.notna().values.flatten()) == 0:
            return f"{FOLDS[fold]} has no value to show", go.Figure(), "", go.Figure()
        if scores_fold.shape[0] > 1:
            titles[
                fold
            ] = f"{FOLDS[fold]}, average {SCORES[targets[0]][metric]} = {pd.Series(scores_fold.loc[:, (targets, fold, metric)].values.flatten()).mean().round(3)} +- {pd.Series(scores_fold.loc[:, (targets, fold, metric)].values.flatten()).std().round(3)}"
        else:
            titles[fold] = FOLDS[fold]

        x_positions = pd.Series(np.arange(5, 10 * len(information.index) + 5, 10), index=information.index)

        figures[fold] = go.Figure()
        figures[fold].update_layout(
            xaxis={
                "tickvals": np.arange(5, 10 * len(information.index) + 5, 10),
                "ticktext": [" - ".join(elem) for elem in information.index],
            }
        )

        for target in targets:
            for algorithm in algorithms:
                if algorithm == "best":
                    indexes = indexes_target_best_algorithms[target]
                    algorithms_custom_data = indexes_target_best_algorithms[target].get_level_values("algorithm")
                else:
                    indexes = (slice(None), slice(None), ALGORITHMS[algorithm])
                    algorithms_custom_data = [ALGORITHMS[algorithm]] * len(information.index)

                customdata = np.dstack(
                    (
                        scores_fold.loc[indexes, (target, fold, f"{metric}_std")].values.flatten(),
                        information[(target, "numbers", "n_participants")].values.flatten(),
                        information[(target, "numbers", "n_variables")].values.flatten(),
                        information[(target, "age_ranges", "min")].values.flatten().astype(int),
                        information[(target, "age_ranges", "max")].values.flatten().astype(int),
                        algorithms_custom_data,
                    )
                )[0]

                figures[fold].add_bar(
                    x=x_positions.loc[information.index].values.flatten(),
                    y=scores_fold.loc[indexes, (target, fold, metric)],
                    error_y={
                        "array": scores_fold.loc[indexes, (target, fold, f"{metric}_std")],
                        "type": "data",
                    },
                    name=f"{TARGETS[target]} {ALGORITHMS[algorithm]}",
                    hovertemplate=hovertemplate,
                    customdata=customdata,
                )

        add_custom_legend_axis(
            figures[fold],
            information.index,
            -120 if metric == "rmse" else -1,
            -60 if metric == "rmse" else -0.5,
            min(scores_fold.loc[:, (targets, fold, metric)].min().min(), 0),
        )

        figures[fold].update_layout(
            yaxis={
                "title": SCORES[targets[0]][metric],
                "showgrid": False,
                "zeroline": False,
                "showticklabels": True,
                "title_font": {"size": 45},
                "dtick": 12 if metric == "rmse" else 0.1,
                "tickfont_size": 20,
            },
            xaxis={"showgrid": False, "zeroline": False},
            height=800,
            margin={"l": 0, "r": 0, "b": 0, "t": 0},
            legend={"orientation": "h", "yanchor": "bottom", "font": {"size": 30}},
        )

    return titles["test"], figures["test"], titles["train"], figures["train"]


LAYOUT = dbc.Container(
    [
        dcc.Loading(
            [
                dcc.Store(id="memory_prediction_performances", data=pd.read_feather(f"data/scores.feather").to_dict()),
                dcc.Store(
                    id="memory_information_prediction_performances",
                    data=pd.read_feather(f"data/information.feather").to_dict(),
                ),
            ]
        ),
        html.H1("Prediction performances"),
        html.Br(),
        html.Br(),
        dbc.Row(dbc.Col(dbc.Card(get_controls_prediction_performances()), width={"size": 4, "offset": 4})),
        html.Br(),
        html.Br(),
        dbc.Col(
            [
                dcc.Loading(
                    [
                        html.H3(id="title_test_prediction_performances"),
                        dcc.Graph(id="bars_test_prediction_performances", config=DOWNLOAD_CONFIG),
                    ]
                )
            ],
            width={"offset": 2},
        ),
        dbc.Col(
            [
                dcc.Loading(
                    [
                        html.H3(id="title_train_prediction_performances"),
                        dcc.Graph(id="bars_train_prediction_performances", config=DOWNLOAD_CONFIG),
                    ]
                )
            ],
            width={"offset": 2},
        ),
    ],
    fluid=True,
)
