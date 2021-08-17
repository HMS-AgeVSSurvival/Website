from website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash
import copy

import pandas as pd
import numpy as np

from website.utils.controls import get_check_list, get_drop_down
from website.utils.rename import rename, rename_index
from website import (
    MAX_LENGTH_CATEGORY,
    TARGETS,
    MAIN_CATEGORIES,
    CATEGORIES,
    ALGORITHMS,
    RANDOM_STATES,
    SCORES_FEATURE_IMPORTANCES,
    DOWNLOAD_CONFIG,
)


@APP.callback(
    Output("memory_feature_importances", "data"),
    [Input(f"{main_category}_category_feature_importances", "value") for main_category in MAIN_CATEGORIES],
)
def get_residual_correlations_all_categories(examination_categories, laboratory_categories, questionnaire_categories):
    if len(examination_categories) == 1:
        main_category = "examination"
        category = examination_categories[0]
    elif len(laboratory_categories) == 1:
        main_category = "laboratory"
        category = laboratory_categories[0]
    elif len(questionnaire_categories) == 1:
        main_category = "questionnaire"
        category = questionnaire_categories[0]
    else:
        raise PreventUpdate

    return pd.read_feather(f"data/feature_importances/{main_category}/{category}.feather").to_dict()


def get_controls_feature_importances():
    categories = copy.deepcopy(CATEGORIES)
    for main_category in MAIN_CATEGORIES:
        del categories[main_category]["all"]

    algorithms = ALGORITHMS.copy()
    del algorithms["best"]

    return (
        [get_check_list("targets_feature_importances", TARGETS, "Target:")]
        + [
            get_drop_down(
                f"{main_category}_category_feature_importances",
                categories[main_category],
                f"{MAIN_CATEGORIES[main_category]} category:",
                multi=True,
                clearable=True,
                value=list(categories[main_category].keys())[0] if main_category == "examination" else [],
            )
            for main_category in MAIN_CATEGORIES
        ]
        + [
            get_check_list(f"algorithm_feature_importances", algorithms, "Algorithm:"),
            get_check_list(f"random_state_feature_importances", RANDOM_STATES, "Random state:"),
        ]
    )


@APP.callback(
    [Output(f"{main_category}_category_feature_importances", "value") for main_category in MAIN_CATEGORIES],
    [Input(f"{main_category}_category_feature_importances", "value") for main_category in MAIN_CATEGORIES],
)
def _update_categories_feature_importances(*args):
    trigger = dash.callback_context.triggered[0]

    if trigger["prop_id"] == ".":
        return args
    else:
        main_categories_values = [[]] * len(MAIN_CATEGORIES)

        if trigger["value"] != []:
            main_categories_values[list(MAIN_CATEGORIES.keys()).index(trigger["prop_id"].split("_")[0])] = [
                trigger["value"][-1]
            ]
        return main_categories_values


@APP.callback(
    [Output("title_train_feature_importances", "children"), Output("bars_train_feature_importances", "figure")],
    [
        Input("memory_feature_importances", "data"),
        Input("memory_scores_feature_importances", "data"),
        Input("targets_feature_importances", "value"),
    ]
    + [Input(f"{main_category}_category_feature_importances", "value") for main_category in MAIN_CATEGORIES]
    + [Input(f"algorithm_feature_importances", "value"), Input(f"random_state_feature_importances", "value")],
)
def _fill_bars_feature_importances(
    feature_importances_data,
    scores_data,
    targets,
    examination_categories,
    laboratory_categories,
    questionnaire_categories,
    algorithms,
    random_states,
):
    import plotly.graph_objs as go
    from website.utils.graphs import add_custom_legend_axis

    if len(targets) == 0:
        return "Please select a target", go.Figure()
    elif len(examination_categories) + len(laboratory_categories) + len(questionnaire_categories) == 0:
        return "Please select a category", go.Figure()
    elif len(algorithms) == 0:
        return "Please select an algorithm", go.Figure()

    if len(examination_categories) == 1:
        category_to_take = ("examination", examination_categories[0])
    elif len(laboratory_categories) == 1:
        category_to_take = ("laboratory", laboratory_categories[0])
    elif len(questionnaire_categories) == 1:
        category_to_take = ("questionnaire", questionnaire_categories[0])
    elif len(random_states) == 0:
        return "Please select a random state", go.Figure()

    scores = pd.DataFrame(scores_data).set_index(["main_category", "category"]).loc[category_to_take]
    scores.index = pd.MultiIndex.from_tuples(
        list(map(eval, scores.index.tolist())), names=["target", "algorithm", "fold", "metric"]
    )

    title = ""
    for target in targets:
        title += f"{TARGETS[target]}: "
        for algorithm in algorithms:
            title += f"for {ALGORITHMS[algorithm]}, "
            metrics = list(SCORES_FEATURE_IMPORTANCES[target].keys())
            for metric in metrics:
                title += f"{SCORES_FEATURE_IMPORTANCES[target][metric]}: {scores.loc[(target, algorithm, 'train', metric)]}, "
            title = title[:-2] + "; "  # Remove ", "
        title = title[:-2] + ". "  # Remove ",

    if len(algorithms) > 1:
        metric = "r2" if "age" in targets else "c_index"
        target = "age" if "age" in targets else targets[0]
        algorithm_to_sort = (
            scores.loc[(target, algorithms, "train", metric)].droplevel(["target", "fold", "metric"]).idxmax()
        )
    else:
        algorithm_to_sort = algorithms[0]

    target_to_sort = "age" if "age" in targets else targets[0]

    feature_importances = (
        pd.DataFrame(feature_importances_data)
        .set_index(["target", "algorithm", "random_state", "predictors"])
        .loc[(targets, algorithms, list(map(int, random_states))), :]
    )
    predictors = (
        feature_importances.loc[(target_to_sort, algorithm_to_sort, int(random_states[0]))]
        .sort_values(["feature_importances"], ascending=False)
        .index.get_level_values("predictors")
        .drop_duplicates()
    )
    capped_predictors = predictors.map(lambda predictor: predictor[:MAX_LENGTH_CATEGORY] + "...")

    hovertemplate = (
        "%{customdata[0]} <Br> Feature importances: %{y:.3f} +- %{customdata[1]:.3f}<extra>%{customdata[2]}</extra>"
    )

    fig = go.Figure()

    for target in targets:
        for algorithm in algorithms:
            for random_state in list(map(int, random_states)):
                customdata = np.dstack(
                    (
                        predictors.values.flatten(),
                        feature_importances.loc[(target, algorithm, random_state, predictors), "std"].values.flatten(),
                        [f"{TARGETS[target]} {ALGORITHMS[algorithm]} {RANDOM_STATES[str(random_state)]}"]
                        * len(predictors),
                    )
                )[0]

                fig.add_bar(
                    x=capped_predictors.values.flatten(),
                    y=feature_importances.loc[
                        (target, algorithm, random_state, predictors), "feature_importances"
                    ].values.flatten(),
                    error_y={
                        "array": feature_importances.loc[
                            (target, algorithm, random_state, predictors), "std"
                        ].values.flatten(),
                        "type": "data",
                    },
                    name=f"{TARGETS[target]} {ALGORITHMS[algorithm]} {RANDOM_STATES[str(random_state)]}",
                    hovertemplate=hovertemplate,
                    customdata=customdata,
                )

    fig.update_layout(
        yaxis={
            "title": "Feature importances",
            "showgrid": False,
            "zeroline": False,
            "showticklabels": True,
            "title_font": {"size": 45},
            "dtick": 0.1,
            "tickfont_size": 20,
        },
        xaxis={"tickangle": 90, "showgrid": False, "zeroline": False},
        height=800,
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
        legend={"orientation": "h", "yanchor": "bottom", "font": {"size": 30}},
    )

    return title, fig


LAYOUT = dbc.Container(
    [
        dcc.Loading(
            [
                dcc.Store(id="memory_feature_importances"),
                dcc.Store(
                    id="memory_scores_feature_importances",
                    data=pd.read_feather(f"data/all_categories/scores_feature_importances.feather").to_dict(),
                ),
            ]
        ),
        html.H1("Feature importances"),
        html.Br(),
        html.Br(),
        dbc.Row(
            dbc.Col(
                dbc.Card(get_controls_feature_importances()),
                width={"size": 4, "offset": 4},
            )
        ),
        html.Br(),
        html.Br(),
        dbc.Col(
            [
                dcc.Loading(
                    [
                        html.H3(id="title_train_feature_importances"),
                        dcc.Graph(id="bars_train_feature_importances", config=DOWNLOAD_CONFIG),
                    ]
                )
            ],
            width={"offset": 2},
        ),
    ],
    fluid=True,
)
