from website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import pandas as pd
import numpy as np

from website.utils.controls import get_item_radio_items, get_check_list, get_drop_down, get_options_from_dict
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
        return ["best"]
    else:
        raise PreventUpdate


@APP.callback(
    [
        Output("title_test_prediction_performances", "children"),
        Output("bars_test_prediction_performances", "figure"),
        Output("title_train_prediction_performances", "children"),
        Output("bars_train_prediction_performances", "figure"),
    ],
    [Input("memory_prediction_performances", "data"), Input("targets_prediction_performances", "value")]
    + [Input(f"{main_category}_category_prediction_performances", "value") for main_category in MAIN_CATEGORIES]
    + [Input(f"algorithm_prediction_performances", "value"), Input(f"metric_prediction_performances", "value")],
)
def _fill_bars_prediction_performances(
    scores_data, targets, examination_categories, laboratory_categories, questionnaire_categories, algorithms, metric
):
    import plotly.graph_objs as go
    from website.utils.graphs import add_custom_legend_axis

    if len(targets) == 0:
        return "Please select a target", go.Figure(), "", go.Figure()
    elif len(examination_categories) + len(laboratory_categories) + len(questionnaire_categories) == 0:
        return "Please select a category", go.Figure(), "", go.Figure()
    elif len(algorithms) == 0:
        return "Please select an algorithm", go.Figure(), "", go.Figure()

    scores_full = pd.DataFrame(scores_data).set_index(["main_category", "category"])
    scores_full.columns = pd.MultiIndex.from_tuples(
        list(map(eval, scores_full.columns.tolist())), names=["target", "algorithm", "fold", "metric"]
    )

    categories_to_display = {
        "examination": examination_categories,
        "laboratory": laboratory_categories,
        "questionnaire": questionnaire_categories,
    }

    indexes_to_take = []
    indexes_to_rename = {}

    if algorithms == ["best"]:
        algorithms = list(ALGORITHMS.keys())
        algorithms.remove("best")
        show_best = True
    else:
        show_best = False

    for main_category in MAIN_CATEGORIES:
        indexes_to_rename[main_category] = MAIN_CATEGORIES[main_category]
        if categories_to_display[main_category] == ["all"]:
            categories_to_display[main_category] = (
                pd.Index(list(CATEGORIES[main_category].keys())).drop("all").to_list()
            )
        for category in categories_to_display[main_category]:
            indexes_to_rename[category] = CATEGORIES[main_category][category]
            indexes_to_take.append([main_category, category])
    for algorithm in algorithms:
        indexes_to_rename[algorithm] = ALGORITHMS[algorithm]

    scores = scores_full.loc[indexes_to_take, (targets, ["numbers", "age_ranges"] + algorithms)]
    if show_best:
        print(scores)
    scores.rename(index=indexes_to_rename, inplace=True)

    if targets != ["age"]:
        scores.replace(-1, np.nan, inplace=True)

    hovertemplate = "%{x},<Br> score: %{y:.3f} +- %{customdata[0]:.3f}, %{customdata[1]} participants with %{customdata[2]} variables, age range %{customdata[3]} to %{customdata[4]} years old <extra>%{customdata[5]}</extra>"

    figures = {}
    titles = {}

    for fold in FOLDS:
        scores_fold = scores.loc[:, (slice(None), slice(None), ["numbers", "age_ranges", fold])].droplevel(
            "fold", axis="columns"
        )

        if scores.shape[0] > 1:
            titles[
                fold
            ] = f"{FOLDS[fold]}, average {SCORES[targets[0]][metric]} = {pd.Series(scores_fold.loc[:, (targets, algorithms, metric)].values.flatten()).mean().round(3)} +- {pd.Series(scores_fold.loc[:, (targets, algorithms, metric)].values.flatten()).std().round(3)}"
        else:
            titles[fold] = FOLDS[fold]

        x_positions = pd.Series(np.arange(5, 10 * len(scores_fold.index) + 5, 10), index=scores_fold.index)

        figures[fold] = go.Figure()
        figures[fold].update_layout(
            xaxis={
                "tickvals": np.arange(5, 10 * len(scores_fold.index) + 5, 10),
                "ticktext": [" - ".join(elem) for elem in scores_fold.index],
            }
        )

        for target in targets:
            for algorithm in algorithms:
                customdata = np.dstack(
                    (
                        scores_fold[(target, algorithm, f"{metric}_std")].values.flatten(),
                        scores_fold[(target, "numbers", "n_participants")].values.flatten(),
                        scores_fold[(target, "numbers", "n_variables")].values.flatten(),
                        scores_fold[(target, "age_ranges", "min")].values.flatten().astype(int),
                        scores_fold[(target, "age_ranges", "max")].values.flatten().astype(int),
                        [ALGORITHMS[algorithm]] * len(scores_fold.index),
                    )
                )[0]

                figures[fold].add_bar(
                    x=x_positions.loc[scores_fold.index].values.flatten(),
                    y=scores_fold[(target, algorithm, metric)],
                    error_y={"array": scores_fold[(target, algorithm, f"{metric}_std")], "type": "data"},
                    name=f"{TARGETS[target]} {ALGORITHMS[algorithm]}",
                    hovertemplate=hovertemplate,
                    customdata=customdata,
                )

        add_custom_legend_axis(
            figures[fold],
            scores_fold.index,
            -120 if metric == "rmse" else -1,
            -60 if metric == "rmse" else -0.5,
            min(scores_fold.loc[:, (targets, algorithms, metric)].min().min(), 0),
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
            dcc.Store(id="memory_prediction_performances", data=pd.read_feather(f"data/scores.feather").to_dict())
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
