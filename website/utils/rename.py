import pandas as pd

from website import TARGETS, MAIN_CATEGORIES, CATEGORIES, CUSTOM_CATEGORIES, ALGORITHMS


def rename(data, custom_categories=True, **kwargs):
    for axis in ["index", "columns"]:
        if kwargs.get(f"{axis}_target", False):
            data.rename(TARGETS, axis=axis, level="target", inplace=True)

        if kwargs.get(f"{axis}_main_category", False):
            data.rename(MAIN_CATEGORIES, axis=axis, level="main_category", inplace=True)

        if kwargs.get(f"{axis}_category", False):
            for main_category in MAIN_CATEGORIES:
                if custom_categories:
                    data.rename(CUSTOM_CATEGORIES[main_category], axis=axis, level="category", inplace=True)
                else:
                    data.rename(CATEGORIES[main_category], axis=axis, level="category", inplace=True)

        if kwargs.get(f"{axis}_algorithm", False):
            data.rename(ALGORITHMS, axis=axis, level="algorithm", inplace=True)


def rename_index(indexes, custom_categories=True, **kwargs):
    data = pd.DataFrame(None, index=indexes)

    if kwargs.get(f"target", False):
        data.rename(index=TARGETS, level="target", inplace=True)

    if kwargs.get(f"main_category", False):
        data.rename(index=MAIN_CATEGORIES, level="main_category", inplace=True)

    if kwargs.get(f"category", False):
        for main_category in MAIN_CATEGORIES:
            if custom_categories:
                data.rename(index=CUSTOM_CATEGORIES[main_category], level="category", inplace=True)
            else:
                data.rename(index=CATEGORIES[main_category], level="category", inplace=True)

    if kwargs.get(f"algorithm", False):
        data.rename(index=ALGORITHMS, level="algorithm", inplace=True)

    return data.index
