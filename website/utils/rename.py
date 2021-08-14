import pandas as pd

from website import TARGETS, MAIN_CATEGORIES, CATEGORIES, CUSTOM_CATEGORIES, ALGORITHMS


def rename(
    data,
    target=False,
    main_category=True,
    category=True,
    algorithm=True,
    index=True,
    columns=True,
    custom_categories=True,
):
    if index:
        if target:
            data.rename(index=TARGETS, level="target", inplace=True)

        if main_category:
            data.rename(index=MAIN_CATEGORIES, level="main_category", inplace=True)

        if category:
            for main_category in MAIN_CATEGORIES:
                if custom_categories:
                    data.rename(index=CUSTOM_CATEGORIES[main_category], level="category", inplace=True)
                else:
                    data.rename(index=CATEGORIES[main_category], level="category", inplace=True)

        if algorithm:
            data.rename(index=ALGORITHMS, level="algorithm", inplace=True)
    if columns:
        if target:
            data.rename(columns=TARGETS, level="target", inplace=True)

        if main_category:
            data.rename(columns=MAIN_CATEGORIES, level="main_category", inplace=True)

        if category:
            for main_category in MAIN_CATEGORIES:
                if custom_categories:
                    data.rename(columns=CUSTOM_CATEGORIES[main_category], level="category", inplace=True)
                else:
                    data.rename(columns=CATEGORIES[main_category], level="category", inplace=True)

        if algorithm:
            data.rename(columns=ALGORITHMS, level="algorithm", inplace=True)


def rename_index(
    indexes, target=False, main_category=True, category=True, algorithm=True, index=True, columns=True, custom_categories=True
):
    data = pd.DataFrame(None, index=indexes)

    if target:
        data.rename(index=TARGETS, level="target", inplace=True)
        
    if main_category:
        data.rename(index=MAIN_CATEGORIES, level="main_category", inplace=True)

    if category:
        for main_category in MAIN_CATEGORIES:
            if custom_categories:
                data.rename(index=CUSTOM_CATEGORIES[main_category], level="category", inplace=True)
            else:
                data.rename(index=CATEGORIES[main_category], level="category", inplace=True)

    if algorithm:
        data.rename(index=ALGORITHMS, level="algorithm", inplace=True)

    return data.index
