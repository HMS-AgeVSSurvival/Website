import pandas as pd
import numpy as np

from website.utils.rename import rename, rename_index
from website import SCORES_FEATURE_IMPORTANCES, TARGETS, MAIN_CATEGORIES, ALGORITHMS, TOO_MANY_CATEGORIES


def plot_feature_importances_correlations(
    feature_importances_correlations_data,
    scores_data,
    information_data,
    targets,
    examination_categories,
    laboratory_categories,
    questionnaire_categories,
    algorithm_a,
    algorithm_b,
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

    categories_to_display = {
        "examination": examination_categories,
        "laboratory": laboratory_categories,
        "questionnaire": questionnaire_categories,
    }

    list_indexes_to_take = []
    for main_category in MAIN_CATEGORIES:
        if categories_to_display[main_category] == ["all"]:
            categories_to_display[main_category] = (
                pd.Index(list(CATEGORIES_IN_DATA[main_category].keys())).drop("all").to_list()
            )
        list_indexes_to_take.extend(
            pd.MultiIndex.from_product(([main_category], categories_to_display[main_category], targets)).to_list()
        )
    indexes_to_take = pd.MultiIndex.from_tuples(list_indexes_to_take, names=["main_category", "category", "target"])
    categories_to_take = indexes_to_take.droplevel("target").drop_duplicates()
    if not custom_categories and len(categories_to_take) > TOO_MANY_CATEGORIES:
        return (
            "Please select less categories, the time required to load the graphs is going to be too long...",
            go.Figure(),
            "",
            go.Figure(),
        )

    scores = pd.DataFrame(scores_data).set_index(["main_category", "category", "algorithm"])
    scores.columns = pd.MultiIndex.from_tuples(
        list(map(eval, scores.columns.tolist())), names=["target", "fold", "metric"]
    )
    information = pd.DataFrame(information_data).set_index(["main_category", "category"])
    information.columns = pd.MultiIndex.from_tuples(
        list(map(eval, information.columns.tolist())), names=["target", "information", "detail"]
    )
    correlations = pd.DataFrame(feature_importances_correlations_data).set_index(
        ["main_category", "category", "target"]
    )
    correlations.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations.columns.tolist())), names=["algorithm_vs_algorithm", "metric"]
    )

    rename(scores, columns=False, custom_categories=custom_categories)
    rename(information, algorithm=False, columns=False, custom_categories=custom_categories)
    rename(correlations, target=True, algorithm=False, columns=False, custom_categories=custom_categories)
    indexes_to_take = rename_index(indexes_to_take, target=True, algorithm=False, custom_categories=custom_categories)
    categories_to_take = rename_index(categories_to_take, algorithm=False, custom_categories=custom_categories)

    if algorithm_a == algorithm_b:
        hovertemplate = (
            "%{x}<Br> correlation: %{y:.3f} +- %{customdata[0]:.3f}<Br> score of "
            + ALGORITHMS[algorithm_a]
            + ": %{customdata[1]:.3f} +- %{customdata[2]:.3f}<Br> %{customdata[3]:.3f} participants with %{customdata[4]} variables, age range %{customdata[5]} to %{customdata[6]} years old <extra>%{customdata[7]}</extra>"
        )
    else:
        hovertemplate = (
            "%{x}<Br> correlation: %{y:.3f} +- %{customdata[0]:.3f}<Br> score of "
            + ALGORITHMS[algorithm_a]
            + ": %{customdata[1]:.3f} +- %{customdata[2]:.3f}, score of "
            + ALGORITHMS[algorithm_b]
            + ": %{customdata[3]:.3f} +- %{customdata[4]:.3f}<Br> %{customdata[5]:.3f} participants with %{customdata[6]} variables, age range %{customdata[7]} to %{customdata[8]} years old <extra>%{customdata[9]}</extra>"
        )

    correlations_to_take = correlations.loc[
        indexes_to_take, (f"{algorithm_a} vs age", "correlation")
    ]  # Replace age with alogithm_b

    if sum(correlations_to_take.notna().values.flatten()) == 0:
        return f"There is no value to show", go.Figure()
    if correlations_to_take.shape[0] > 1:
        title = f"Average correlation = {correlations_to_take.values.flatten().mean().round(3)} +- {correlations_to_take.values.flatten().std().round(3)}"
    else:
        title = f"Correlation between {algorithm_a} and {algorithm_b}"

    x_positions = pd.Series(np.arange(5, 10 * len(categories_to_take) + 5, 10), index=categories_to_take)

    fig = go.Figure()
    fig.update_layout(
        xaxis={
            "tickvals": np.arange(5, 10 * len(categories_to_take) + 5, 10),
            "ticktext": [" - ".join(elem) for elem in categories_to_take],
        }
    )

    for target in targets:
        metric = list(SCORES_FEATURE_IMPORTANCES[target].keys())[0]
        if algorithm_a == algorithm_b:
            customdata = np.dstack(
                (
                    correlations_to_take[(f"{algorithm_a} vs {target}", "std")],  # Replace target with alogithm_b
                    scores.loc[indexes_to_take, (target, "train", f"{metric}")].values.flatten(),
                    scores.loc[indexes_to_take, (target, "train", f"{metric}_std")].values.flatten(),
                    information.loc[categories_to_take, (target, "numbers", "n_participants")].values.flatten(),
                    information.loc[categories_to_take, (target, "numbers", "n_variables")].values.flatten(),
                    information.loc[categories_to_take, (target, "age_ranges", "min")].values.flatten().astype(int),
                    information.loc[categories_to_take, (target, "age_ranges", "max")].values.flatten().astype(int),
                    [TARGETS[target]] * len(categories_to_take),
                )
            )[0]

            fig.add_bar(
                x=x_positions.values.flatten(),
                y=correlations_to_take[(f"{algorithm_a} vs {target}", "correlation")],  # Replace target with alogithm_b
                error_y={
                    "array": correlations_to_take[(f"{algorithm_a} vs {target}", "std")],
                    "type": "data",
                },
                name=TARGETS[target],
                hovertemplate=hovertemplate,
                customdata=customdata,
            )

    add_custom_legend_axis(
        fig,
        categories_to_take,
        -1,
        -0.5,
        min(correlations_to_take.min().min(), 0),
    )

    fig.update_layout(
        yaxis={
            "title": "Correlations",
            "showgrid": False,
            "zeroline": False,
            "showticklabels": True,
            "title_font": {"size": 45},
            "dtick": 0.1,
            "tickfont_size": 20,
        },
        xaxis={"showgrid": False, "zeroline": False},
        height=800,
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
        legend={"orientation": "h", "yanchor": "bottom", "font": {"size": 30}},
    )

    return title, fig