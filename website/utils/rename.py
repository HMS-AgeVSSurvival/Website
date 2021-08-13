import pandas as pd

from website import MAIN_CATEGORIES, CATEGORIES, CUSTOM_CATEGORIES, ALGORITHMS


def rename(data, main_category=True, category=True, algorithm=True, index=True, columns=True, custom_categories=True):
    if index:
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
    indexes, main_category=True, category=True, algorithm=True, index=True, columns=True, custom_categories=True
):
    data = pd.DataFrame(None, index=indexes)

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
