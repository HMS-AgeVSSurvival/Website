import pandas as pd
import numpy as np

from website.utils.rename import rename, rename_index
from website import (
    TARGETS,
    MAIN_CATEGORIES,
    ALGORITHMS,
    SCORES_FEATURE_IMPORTANCES,
    TOO_MANY_CATEGORIES,
)


def plot_feature_importances_correlations(
    feature_importances_correlations_data,
    scores_data,
    information_data,
    target_a,
    target_b,
    examination_categories,
    laboratory_categories,
    questionnaire_categories,
    algorithms,
    custom_categories=True,
):
    import plotly.graph_objs as go
    from website.utils.graphs import add_custom_legend_axis

    if custom_categories:
        from website import CUSTOM_CATEGORIES as CATEGORIES_IN_DATA
    else:
        from website import CATEGORIES as CATEGORIES_IN_DATA

    if len(examination_categories) + len(laboratory_categories) + len(questionnaire_categories) == 0:
        return "Please select a category", go.Figure()
    elif len(algorithms) == 0:
        return "Please select an algorithm", go.Figure()

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
        )

    correlations = (
        pd.DataFrame(feature_importances_correlations_data)
        .set_index(["main_category", "category"])
        .loc[categories_to_take]
    )
    correlations.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations.columns.tolist())), names=["targets", "algorithm", "metric"]
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
        correlations,
        index_main_category=True,
        index_category=True,
        columns_algorithm=True,
        custom_categories=custom_categories,
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

    if target_a == target_b:
        hovertemplate = (
            "%{x} <Br>Correlation %{y:.3f} +- %{customdata[0]:.3f} <Br><Br>"
            + TARGETS[target_a]
            + " score: %{customdata[1]:.3f} +- %{customdata[2]:.3f} <Br><Br>%{customdata[3]} participants with %{customdata[4]} variables, age range %{customdata[5]} to %{customdata[6]} years old <extra>%{customdata[7]}</extra>"
        )
    else:
        hovertemplate = (
            "%{x} <Br>Correlation %{y:.3f} +- %{customdata[0]:.3f} <Br><Br>"
            + TARGETS[target_a]
            + " score: %{customdata[1]:.3f} +- %{customdata[2]:.3f} <Br>%{customdata[3]} participants with %{customdata[4]} variables, age range %{customdata[5]} to %{customdata[6]} years old<Br><Br>"
            + TARGETS[target_b]
            + " score: %{customdata[7]:.3f} +- %{customdata[8]:.3f} <Br>%{customdata[9]} participants with %{customdata[10]} variables, age range %{customdata[11]} to %{customdata[12]} years old <extra>%{customdata[13]}</extra>"
        )

    x_positions = pd.Series(np.arange(5, 10 * len(categories_to_take) + 5, 10), index=categories_to_take)

    fig = go.Figure()
    fig.update_layout(
        xaxis={
            "tickvals": np.arange(5, 10 * len(categories_to_take) + 5, 10),
            "ticktext": [" - ".join(elem) for elem in categories_to_take],
        }
    )

    shown_correlations = []

    for algorithm in algorithms:
        metric_a = list(SCORES_FEATURE_IMPORTANCES[target_a].keys())[0]
        metric_b = list(SCORES_FEATURE_IMPORTANCES[target_b].keys())[0]

        if algorithm == "best":
            best_algorithms_a = (
                scores.loc[:, (TARGETS[target_a], slice(None), "train", metric_a)]
                .droplevel(["target", "fold", "metric"], axis=1)
                .idxmax(axis=1)
            ).replace(np.nan, list(ALGORITHMS.values())[0])
            main_categories_categories_best_algorithms_a = best_algorithms_a.reset_index().apply(
                lambda x: tuple(x), axis=1
            )

            correlations_values = (
                correlations.loc[:, (f"{target_a} vs {target_b}", slice(None), "correlation")]
                .stack(level="algorithm", dropna=False)
                .loc[main_categories_categories_best_algorithms_a]
            ).values.flatten()
            correlations_std = (
                correlations.loc[:, (f"{target_a} vs {target_b}", slice(None), "std")]
                .stack(level="algorithm", dropna=False)
                .loc[main_categories_categories_best_algorithms_a]
            ).values.flatten()
            scores_a_values = (
                scores.loc[:, (TARGETS[target_a], slice(None), "train", metric_a)]
                .stack(level="algorithm", dropna=False)
                .loc[main_categories_categories_best_algorithms_a]
            ).values.flatten()
            scores_a_std = (
                scores.loc[:, (TARGETS[target_a], slice(None), "train", f"{metric_a}_std")]
                .stack(level="algorithm", dropna=False)
                .loc[main_categories_categories_best_algorithms_a]
            ).values.flatten()
            algorithms_custom_data_a = best_algorithms_a.values.flatten()

            if target_a != target_b:
                scores_b_values = (
                    scores.loc[:, (TARGETS[target_b], slice(None), "train", metric_b)]
                    .stack(level="algorithm", dropna=False)
                    .loc[main_categories_categories_best_algorithms_a]
                ).values.flatten()
                scores_b_std = (
                    scores.loc[:, (TARGETS[target_b], slice(None), "train", f"{metric_b}_std")]
                    .stack(level="algorithm", dropna=False)
                    .loc[main_categories_categories_best_algorithms_a]
                ).values.flatten()
        else:
            correlations_values = correlations[
                (f"{target_a} vs {target_b}", ALGORITHMS[algorithm], "correlation")
            ].values.flatten()
            correlations_std = correlations[
                (f"{target_a} vs {target_b}", ALGORITHMS[algorithm], "std")
            ].values.flatten()
            scores_a_values = scores[(TARGETS[target_a], ALGORITHMS[algorithm], "train", metric_a)].values.flatten()
            scores_a_std = scores[
                (TARGETS[target_a], ALGORITHMS[algorithm], "train", f"{metric_a}_std")
            ].values.flatten()
            algorithms_custom_data_a = [ALGORITHMS[algorithm]] * len(categories_to_take)

            if target_a != target_b:
                scores_b_values = scores[(TARGETS[target_b], ALGORITHMS[algorithm], "train", metric_b)].values.flatten()
                scores_b_std = scores[
                    (TARGETS[target_b], ALGORITHMS[algorithm], "train", f"{metric_b}_std")
                ].values.flatten()

        if target_a == target_b:
            customdata = np.dstack(
                (
                    correlations_std,
                    scores_a_values,
                    scores_a_std,
                    information[(TARGETS[target_a], "numbers", "n_participants")].values.flatten(),
                    information[(TARGETS[target_a], "numbers", "n_variables")].values.flatten(),
                    information[(TARGETS[target_a], "age_ranges", "min")].values.flatten().astype(int),
                    information[(TARGETS[target_a], "age_ranges", "max")].values.flatten().astype(int),
                    algorithms_custom_data_a,
                )
            )[0]
        else:
            customdata = np.dstack(
                (
                    correlations_std,
                    scores_a_values,
                    scores_a_std,
                    information[(TARGETS[target_a], "numbers", "n_participants")].values.flatten(),
                    information[(TARGETS[target_a], "numbers", "n_variables")].values.flatten(),
                    information[(TARGETS[target_a], "age_ranges", "min")].values.flatten().astype(int),
                    information[(TARGETS[target_a], "age_ranges", "max")].values.flatten().astype(int),
                    scores_b_values,
                    scores_b_std,
                    information[(TARGETS[target_b], "numbers", "n_participants")].values.flatten(),
                    information[(TARGETS[target_b], "numbers", "n_variables")].values.flatten(),
                    information[(TARGETS[target_b], "age_ranges", "min")].values.flatten().astype(int),
                    information[(TARGETS[target_b], "age_ranges", "max")].values.flatten().astype(int),
                    algorithms_custom_data_a,
                )
            )[0]

        fig.add_bar(
            x=x_positions.values.flatten(),
            y=correlations_values,
            error_y={
                "array": correlations_std,
                "type": "data",
            },
            name=f"{ALGORITHMS[algorithm]}",
            hovertemplate=hovertemplate,
            customdata=customdata,
        )

        shown_correlations.extend(correlations_values)

    if pd.Series(shown_correlations).notna().sum() == 0:
        return "These settings have no value to show, consider changing the targets or the categories", go.Figure()

    add_custom_legend_axis(
        fig,
        categories_to_take,
        -1,
        -0.5,
        min(pd.Series(shown_correlations).min(), 0),
    )

    title = f"Average correlation = {pd.Series(shown_correlations).mean().round(3)} +- {pd.Series(shown_correlations).std().round(3)}"

    fig.update_layout(
        yaxis={
            "title": "Correlation",
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
