# Welcome to the repository of the [Website](https://prod---website-vbip4gqz2q-uc.a.run.app) that shows the paper's results

[![Website](https://img.shields.io/website?up_color=green&url=https%3A%2F%2Fprod---website-vbip4gqz2q-uc.a.run.app%2F)](https://prod---website-vbip4gqz2q-uc.a.run.app/)
[![Super linter](https://github.com/HMS-Internship/Website/actions/workflows/linter.yml/badge.svg)](https://github.com/HMS-Internship/Website/actions/workflows/linter.yml)

The website is coded in Python, using the framework Dash. The data is stored on AWS s3. We use Cloud Run from Google Cloud Platform to host our website.

## Contribute to the project

The fact that you cannot have access to the data stored on AWS (since we don't share the credentials) makes it harder to contribute to the project. However, you can still propose the some changes with a pull request.

Once you have forked the repository and cloned it, you can install the package with its development dependencies using:
```bash
pip install -e .[env]
```

The command `launch_local_website` allows you to test the website locally.

If you are using Visual Studio Code, a [.devcontainer](/.devcontainer) folder is already prepared so that you can work in a dedicated container.

Feel free to discuss about you ideas in the [discussion section](https://github.com/HMS-Internship/Website/discussions).

## Structure of website's code
```bash
📦Website
 ┣ 📂.devcontainer
 ┃ ┣ 📜Dockerfile
 ┃ ┗ 📜devcontainer.json
 ┣ 📂post_processing
 ┃ ┣ 📂all_categories
 ┃ ┃ ┣ 📜feature_importances_correlation.py
 ┃ ┃ ┣ 📜information.py
 ┃ ┃ ┣ 📜scores_feature_importances.py
 ┃ ┃ ┗ 📜scores_residual.py
 ┃ ┣ 📂custom_categories
 ┃ ┃ ┣ 📜create_custom_data.py
 ┃ ┃ ┗ 📜select_categories.py
 ┃ ┗ 📜__init__.py
 ┣ 📂website
 ┃ ┣ 📂dataset
 ┃ ┃ ┗ 📜page.py
 ┃ ┣ 📂feature_importances
 ┃ ┃ ┗ 📜page.py
 ┃ ┣ 📂feature_importances_correlations
 ┃ ┃ ┣ 📂between_algorithms
 ┃ ┃ ┃ ┣ 📂tabs
 ┃ ┃ ┃ ┃ ┣ 📜all_categories.py
 ┃ ┃ ┃ ┃ ┣ 📜custom_categories.py
 ┃ ┃ ┃ ┃ ┗ 📜shared_plotter.py
 ┃ ┃ ┃ ┗ 📜page.py
 ┃ ┃ ┗ 📂between_targets
 ┃ ┃ ┃ ┣ 📂tabs
 ┃ ┃ ┃ ┃ ┣ 📜all_categories.py
 ┃ ┃ ┃ ┃ ┣ 📜custom_categories.py
 ┃ ┃ ┃ ┃ ┗ 📜shared_plotter.py
 ┃ ┃ ┃ ┗ 📜page.py
 ┃ ┣ 📂prediction_performances
 ┃ ┃ ┣ 📂feature_importances
 ┃ ┃ ┃ ┣ 📂tabs
 ┃ ┃ ┃ ┃ ┣ 📜all_categories.py
 ┃ ┃ ┃ ┃ ┣ 📜custom_categories.py
 ┃ ┃ ┃ ┃ ┗ 📜shared_plotter.py
 ┃ ┃ ┃ ┗ 📜page.py
 ┃ ┃ ┗ 📂residual
 ┃ ┃ ┃ ┣ 📂tabs
 ┃ ┃ ┃ ┃ ┣ 📜all_categories.py
 ┃ ┃ ┃ ┃ ┣ 📜custom_categories.py
 ┃ ┃ ┃ ┃ ┗ 📜shared_plotter.py
 ┃ ┃ ┃ ┗ 📜page.py
 ┃ ┣ 📂residual_correlations
 ┃ ┃ ┣ 📂tabs
 ┃ ┃ ┃ ┣ 📜all_categories.py
 ┃ ┃ ┃ ┣ 📜custom_categories.py
 ┃ ┃ ┃ ┗ 📜share_plotter.py
 ┃ ┃ ┗ 📜page.py
 ┃ ┣ 📂utils
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜aws_loader.py
 ┃ ┃ ┣ 📜controls.py
 ┃ ┃ ┣ 📜graphs.py
 ┃ ┃ ┗ 📜rename.py
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜app.py
 ┃ ┣ 📜index.py
 ┃ ┗ 📜introduction.py
 ┣ 📜.dockerignore
 ┣ 📜.gitignore
 ┣ 📜Dockerfile
 ┣ 📜LICENSE
 ┣ 📜README.md
 ┗ 📜setup.py
```

## Structure of the website's data (on AWS s3)
```Bash
📦age-vs-survival
 ┣ 📂all_categories
 ┃ ┣ 📂correlations
 ┃ ┃ ┣ 📂feature_importances
 ┃ ┃ ┃ ┣ 📜pearson_between_algorithms.feather
 ┃ ┃ ┃ ┣ 📜pearson_between_targets.feather
 ┃ ┃ ┃ ┣ 📜pearson_[...].feather  # Original data not used in website
 ┃ ┃ ┃ ┣ 📜spearman_between_algorithms.feather
 ┃ ┃ ┃ ┣ 📜spearman_between_targets.feather
 ┃ ┃ ┃ ┗ 📜spearman_[...].feather  # Original data not used in website  # Original data not used in website
 ┃ ┃ ┗ 📂residual
 ┃ ┃   ┣ 📜number_participants_[...].feather
 ┃ ┃   ┣ 📜pearson_[...].feather
 ┃ ┃   ┗ 📜spearman_[...].feather
 ┃ ┣ 📜information.feather
 ┃ ┣ 📜scores_feature_importances.feather
 ┃ ┗ 📜scores_residual.feather
 ┣ 📂custom_categories
 ┃ ┣ 📂correlations
 ┃ ┃ ┣ 📂feature_importances
 ┃ ┃ ┃ ┣ 📜pearson_between_algorithms.feather
 ┃ ┃ ┃ ┣ 📜pearson_between_targets.feather
 ┃ ┃ ┃ ┣ 📜spearman_between_algorithms.feather
 ┃ ┃ ┃ ┗ 📜spearman_between_targets.feather
 ┃ ┃ ┗ 📂residual
 ┃ ┃   ┣ 📜number_participants_[...].feather
 ┃ ┃   ┣ 📜pearson_[...].feather
 ┃ ┃   ┗ 📜spearman_[...].feather
 ┃ ┣ 📜information.feather
 ┃ ┣ 📜scores_feature_importances.feather
 ┃ ┗ 📜scores_residual.feather
 ┣ 📂examination
 ┃ ┗ 📜category.feather
 ┣ 📂feature_importances
 ┃ ┣ 📂examination
 ┃ ┃ ┗ 📜category.feather
 ┃ ┣ 📂laboratory
 ┃ ┃ ┗ 📜category.feather
 ┃ ┗ 📂questionnaire
 ┃   ┗ 📜category.feather
 ┣ 📂laboratory
 ┃ ┗ 📜category.feather
 ┣ 📂questionnaire
 ┃ ┗ 📜category.feather
 ┣ 📜Results.xlsx  # Original data not used in website
 ┗ 📜favicon.ico
```

## How to deploy

A CI / CD workflow has been created with Git Actions in order to deploy the website automatically on demand. You can find the development version of the website [here](https://dev---website-vbip4gqz2q-uc.a.run.app/).

## How to update the data

Under the folder __data__, the files that can be updated are the following:
- Results.xlsx
- correlations/feature_importances/correlation_type_main_category.feather
- correlations/feature_importances/correlation_type_std_main_category.feather
- correlations/residual/number_participants_type_of_death_type_of_death.feather
- correlations/residual/correlation_type_type_of_death_type_of_death.feather
- main_category/category.feather

To generate the other files, all the scripts under the folder __data__ has to be executed.
The file [select_categories.py](./post_processing/custom_categories/select_categories.py) outputs the 30 best models. This list has to match with the list called *CUSTOM_CATEGORIES_INDEX* in the [website code](./website/__init__.py).

Once everything is done, don't forget to push the new \_\_init__.py file to GitHub, to push the new data the AWS s3 so that you can use the CI / CD pipeline.

To sync the __data__ folder to AWS s3, you can use the following:
```bash
aws s3 sync data/ age-vs-survival/ --delete
```