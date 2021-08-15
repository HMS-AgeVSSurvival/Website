import pandas as pd
import numpy as np

from website.utils.rename import rename, rename_index
from website import TARGETS, MAIN_CATEGORIES, ALGORITHMS, FOLDS_RESIDUAL, SCORES_RESIDUAL, TOO_MANY_CATEGORIES


def plot_scores(
    scores_data,
    information_data,
    targets,
    examination_categories,
    laboratory_categories,
    questionnaire_categories,
    algorithms,
    metric,
    custom_categories=True,
):
    import plotly.graph_objs as go
    from website.utils.graphs import add_custom_legend_axis

    if custom_categories:
        from website import CUSTOM_CATEGORIES as CATEGORIES_IN_DATA
    else:
        from website import CATEGORIES as CATEGORIES_IN_DATA

    if len(targets) == 0:
        return "Please select a target", go.Figure(), "", go.Figure()
    elif len(examination_categories) + len(laboratory_categories) + len(questionnaire_categories) == 0:
        return "Please select a category", go.Figure(), "", go.Figure()
    elif len(algorithms) == 0:
        return "Please select an algorithm", go.Figure(), "", go.Figure()

    categories_to_display = {
        "examination": examination_categories,
        "laboratory": laboratory_categories,
        "questionnaire": questionnaire_categories,
    }

    list_categories_to_take = []
    for main_category in MAIN_CATEGORIES:
        if categories_to_display[main_category] == ["all"]:
            categories_to_display[main_category] = (
                pd.Index(list(CATEGORIES_IN_DATA[main_category].keys())).drop("all").to_list()
            )
        list_categories_to_take.extend(
            pd.MultiIndex.from_product(([main_category], categories_to_display[main_category])).to_list()
        )
    categories_to_take = pd.MultiIndex.from_tuples(list_categories_to_take, names=["main_category", "category"])
    if not custom_categories and len(categories_to_take) > TOO_MANY_CATEGORIES:
        return (
            "Please select less categories, the time required to load the graphs is going to be too long...",
            go.Figure(),
            "",
            go.Figure(),
        )

    scores = pd.DataFrame(scores_data).set_index(["main_category", "category"]).loc[categories_to_take]
    scores.columns = pd.MultiIndex.from_tuples(
        list(map(eval, scores.columns.tolist())), names=["target", "algorithm", "fold", "metric"]
    )
    information = pd.DataFrame(information_data).set_index(["main_category", "category"]).loc[categories_to_take]
    information.columns = pd.MultiIndex.from_tuples(
        list(map(eval, information.columns.tolist())), names=["target", "information", "detail"]
    )

    rename(
        scores,
        index_main_category=True,
        index_category=True,
        columns_target=True,
        columns_algorithm=True,
        custom_categories=custom_categories,
    )
    rename(
        information,
        index_main_category=True,
        index_category=True,
        columns_target=True,
        custom_categories=custom_categories,
    )
    categories_to_take = rename_index(
        categories_to_take, main_category=True, category=True, custom_categories=custom_categories
    )

    hovertemplate = "%{x},<Br> score: %{y:.3f} +- %{customdata[0]:.3f}, %{customdata[1]} participants with %{customdata[2]} variables, age range %{customdata[3]} to %{customdata[4]} years old <extra>%{customdata[5]}</extra>"

    figures = {}
    titles = {}

    for fold in FOLDS_RESIDUAL:
        x_positions = pd.Series(np.arange(5, 10 * len(categories_to_take) + 5, 10), index=categories_to_take)

        figures[fold] = go.Figure()
        figures[fold].update_layout(
            xaxis={
                "tickvals": np.arange(5, 10 * len(categories_to_take) + 5, 10),
                "ticktext": [" - ".join(elem) for elem in categories_to_take],
            }
        )

        shown_scores = []

        for target in targets:
            for algorithm in algorithms:
                if algorithm == "best":
                    best_algorithms = (
                        scores.loc[:, (TARGETS[target], slice(None), "test", metric)]
                        .droplevel(["target", "fold", "metric"], axis=1)
                        .idxmax(axis=1)
                    ).replace(np.nan, list(ALGORITHMS.values())[0])
                    main_categories_categories_best_algorithms = best_algorithms.reset_index().apply(
                        lambda x: tuple(x), axis=1
                    )
                    scores_values = (
                        scores.loc[:, (TARGETS[target], slice(None), fold, metric)]
                        .stack(level="algorithm", dropna=False)
                        .loc[main_categories_categories_best_algorithms]
                    ).values.flatten()
                    scores_std = (
                        scores.loc[:, (TARGETS[target], slice(None), fold, f"{metric}_std")]
                        .stack(level="algorithm", dropna=False)
                        .loc[main_categories_categories_best_algorithms]
                    ).values.flatten()
                    algorithms_custom_data = best_algorithms.values.flatten()
                else:
                    scores_values = scores[(TARGETS[target], ALGORITHMS[algorithm], fold, metric)].values
                    scores_std = scores[(TARGETS[target], ALGORITHMS[algorithm], fold, f"{metric}_std")].values
                    algorithms_custom_data = [ALGORITHMS[algorithm]] * len(categories_to_take)

                customdata = np.dstack(
                    (
                        scores_std.flatten(),
                        information[(TARGETS[target], "numbers", "n_participants")].values.flatten(),
                        information[(TARGETS[target], "numbers", "n_variables")].values.flatten(),
                        information[(TARGETS[target], "age_ranges", "min")].values.flatten().astype(int),
                        information[(TARGETS[target], "age_ranges", "max")].values.flatten().astype(int),
                        algorithms_custom_data,
                    )
                )[0]

                figures[fold].add_bar(
                    x=x_positions.values.flatten(),
                    y=scores_values,
                    error_y={
                        "array": scores_std,
                        "type": "data",
                    },
                    name=f"{TARGETS[target]} {ALGORITHMS[algorithm]}",
                    hovertemplate=hovertemplate,
                    customdata=customdata,
                )

                shown_scores.extend(scores_values.flatten())

        if pd.Series(shown_scores).notna().sum() == 0:
            return f"{FOLDS_RESIDUAL[fold]} has no value to show", go.Figure(), "", go.Figure()

        add_custom_legend_axis(
            figures[fold],
            categories_to_take,
            -120 if metric == "rmse" else -1,
            -60 if metric == "rmse" else -0.5,
            min(pd.Series(shown_scores).min(), 0),
        )

        titles[
            fold
        ] = f"{FOLDS_RESIDUAL[fold]}, average {SCORES_RESIDUAL[targets[0]][metric]} = {pd.Series(shown_scores).mean().round(3)} +- {pd.Series(shown_scores).std().round(3)}"

        figures[fold].update_layout(
            yaxis={
                "title": SCORES_RESIDUAL[targets[0]][metric],
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
