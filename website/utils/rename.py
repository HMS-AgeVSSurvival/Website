from website import MAIN_CATEGORIES, CATEGORIES, ALGORITHMS


def rename(data, main_category=True, category=True, algorithm=True, index=True, columns=True):
    if index:
        if main_category:
            data.rename(index=MAIN_CATEGORIES, level="main_category", inplace=True)

        if category:
            for main_category in MAIN_CATEGORIES:
                data.rename(index=CATEGORIES[main_category], level="category", inplace=True)

        if algorithm:
            data.rename(index=ALGORITHMS, level="algorithm", inplace=True)
    if columns:
        if main_category:
            data.rename(columns=MAIN_CATEGORIES, level="main_category", inplace=True)

        if category:
            for main_category in MAIN_CATEGORIES:
                data.rename(columns=CATEGORIES[main_category], level="category", inplace=True)

        if algorithm:
            data.rename(columns=ALGORITHMS, level="algorithm", inplace=True)
