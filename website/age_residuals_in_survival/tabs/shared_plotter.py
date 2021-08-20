import pandas as pd
import numpy as np

from website.utils.rename import rename, rename_index
from website import TARGETS, MAIN_CATEGORIES, ALGORITHMS, TOO_MANY_CATEGORIES


def plot_log_hazard_ratio(
    log_hazard_ratio_data,
    scores_data,
    information_data,
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

    log_hazard_ratio = (
        pd.DataFrame(log_hazard_ratio_data).set_index(["main_category", "category"]).loc[categories_to_take]
    )
    log_hazard_ratio.columns = pd.MultiIndex.from_tuples(
        list(map(eval, log_hazard_ratio.columns.tolist())), names=["algorithm", "metric"]
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
        log_hazard_ratio,
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

    hovertemplate = "%{x} <Br>Log hazard ratio %{y:3f} +- %{customdata[0]:.3f} with a p-value of %{customdata[1]:.3f} <Br>R² %{customdata[2]:.3f} +- %{customdata[3]:.3f}, %{customdata[4]} participants with %{customdata[5]} variables, age range %{customdata[6]} to %{customdata[7]} years old <extra>%{customdata[8]}</extra>"

    x_positions = pd.Series(np.arange(5, 10 * len(categories_to_take) + 5, 10), index=categories_to_take)

    fig = go.Figure()
    fig.update_layout(
        xaxis={
            "tickvals": np.arange(5, 10 * len(categories_to_take) + 5, 10),
            "ticktext": [" - ".join(elem) for elem in categories_to_take],
        }
    )

    shown_log_hazard_ratio = []

    for algorithm in algorithms:
        if algorithm == "best":
            best_algorithms = (
                scores.loc[:, (TARGETS["age"], slice(None), "test", "r2")]
                .droplevel(["target", "fold", "metric"], axis=1)
                .idxmax(axis=1)
            ).replace(np.nan, list(ALGORITHMS.values())[0])
            main_categories_categories_best_algorithms = best_algorithms.reset_index().apply(lambda x: tuple(x), axis=1)
            log_hazard_ratio_values = (
                log_hazard_ratio.loc[:, (slice(None), "log_hazard_ratio")]
                .stack(level="algorithm", dropna=False)
                .loc[main_categories_categories_best_algorithms]
            ).values.flatten()
            log_hazard_ratio_std = (
                log_hazard_ratio.loc[:, (slice(None), "std")]
                .stack(level="algorithm", dropna=False)
                .loc[main_categories_categories_best_algorithms]
            ).values.flatten()
            log_hazard_ratio_p_values = (
                log_hazard_ratio.loc[:, (slice(None), "p_value")]
                .stack(level="algorithm", dropna=False)
                .loc[main_categories_categories_best_algorithms]
            ).values.flatten()
            scores_values = (
                scores.loc[:, (TARGETS["age"], slice(None), "test", "r2")]
                .stack(level="algorithm", dropna=False)
                .loc[main_categories_categories_best_algorithms]
            ).values.flatten()
            scores_std = (
                scores.loc[:, (TARGETS["age"], slice(None), "test", "r2_std")]
                .stack(level="algorithm", dropna=False)
                .loc[main_categories_categories_best_algorithms]
            ).values.flatten()
            algorithms_custom_data = best_algorithms.values.flatten()
        else:
            log_hazard_ratio_values = log_hazard_ratio[(ALGORITHMS[algorithm], "log_hazard_ratio")].values
            log_hazard_ratio_std = log_hazard_ratio[(ALGORITHMS[algorithm], "std")].values
            log_hazard_ratio_p_values = log_hazard_ratio[(ALGORITHMS[algorithm], "p_value")].values
            scores_values = scores[(TARGETS["age"], ALGORITHMS[algorithm], "test", "r2")].values
            scores_std = scores[(TARGETS["age"], ALGORITHMS[algorithm], "test", "r2")].values
            algorithms_custom_data = [ALGORITHMS[algorithm]] * len(categories_to_take)

        customdata = np.dstack(
            (
                log_hazard_ratio_std.flatten(),
                log_hazard_ratio_p_values.flatten(),
                scores_values.flatten(),
                scores_std.flatten(),
                information[(TARGETS["age"], "numbers", "n_participants")].values.flatten(),
                information[(TARGETS["age"], "numbers", "n_variables")].values.flatten(),
                information[(TARGETS["age"], "age_ranges", "min")].values.flatten().astype(int),
                information[(TARGETS["age"], "age_ranges", "max")].values.flatten().astype(int),
                algorithms_custom_data,
            )
        )[0]

        fig.add_bar(
            x=x_positions.values.flatten(),
            y=log_hazard_ratio_values,
            error_y={
                "array": log_hazard_ratio_std,
                "type": "data",
            },
            name=f"{ALGORITHMS[algorithm]}",
            hovertemplate=hovertemplate,
            customdata=customdata,
        )

        shown_log_hazard_ratio.extend(log_hazard_ratio_values.flatten() - np.abs(log_hazard_ratio_std.flatten()))

    if pd.Series(shown_log_hazard_ratio).notna().sum() == 0:
        return f"There is no value to show", go.Figure()

    min_shown_value = min(pd.Series(shown_log_hazard_ratio).min(), 0)

    add_custom_legend_axis(
        fig,
        categories_to_take,
        -1 + min_shown_value,
        -0.5 + min_shown_value,
        min_shown_value,
    )

    title = f"Average log hazard ratio = {pd.Series(shown_log_hazard_ratio).mean().round(3)} +- {pd.Series(shown_log_hazard_ratio).std().round(3)}"

    fig.update_layout(
        yaxis={
            "title": "Log hazard ratio",
            "showgrid": False,
            "zeroline": False,
            "showticklabels": True,
            "title_font": {"size": 45},
            "tickfont_size": 20,
        },
        xaxis={"showgrid": False, "zeroline": False},
        height=800,
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
        legend={"orientation": "h", "yanchor": "bottom", "font": {"size": 30}},
    )

    return title, fig
