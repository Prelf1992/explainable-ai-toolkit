
# Explainable AI Toolkit

A collection of tools and examples for interpreting and explaining predictions from complex machine learning models, focusing on LIME and SHAP.

## Features

*   **LIME Integration:** Local Interpretable Model-agnostic Explanations for black-box models.
*   **SHAP Integration:** SHapley Additive exPlanations for unified feature attribution.
*   **Visualization Tools:** Interactive plots for understanding model decisions.
*   **Framework Agnostic:** Works with various ML frameworks (Scikit-learn, TensorFlow, PyTorch).

## Technologies Used

*   Python
*   Scikit-learn
*   TensorFlow/PyTorch (examples)
*   LIME
*   SHAP

## Getting Started

### Installation

```bash
git clone https://github.com/Prelf1992/explainable-ai-toolkit.git
cd explainable-ai-toolkit
pip install -r requirements.txt
```

### Usage

```python
import lime
import lime.lime_tabular
import shap
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

# Generate synthetic data
X, y = make_classification(n_samples=100, n_features=10, n_informative=5, n_redundant=0, random_state=42)

# Train a black-box model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# LIME Explainer
explainer_lime = lime.lime_tabular.LimeTabularExplainer(
    training_data=X,
    feature_names=[f'feature_{i}' for i in range(X.shape[1])],
    class_names=['class_0', 'class_1'],
    mode='classification'
)
explanation_lime = explainer_lime.explain_instance(
    data_row=X[0],
    predict_fn=model.predict_proba,
    num_features=5
)
print("LIME Explanation:")
explanation_lime.show_in_note()

# SHAP Explainer
explainer_shap = shap.TreeExplainer(model)
shap_values = explainer_shap.shap_values(X)
print("
SHAP Explanation (first instance):
", shap_values[0])

shap.summary_plot(shap_values, X, feature_names=[f'feature_{i}' for i in range(X.shape[1])])
```

## Contributing

We welcome contributions! Please see `CONTRIBUTING.md` for details.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
* Commit 1: Chore: Update build config tests to align with standards. at 2024-11-01 14:37:59
* Commit 2: Style: Update documentation for README to improve user experience. at 2024-11-01 17:59:40
* Commit 3: Test: Improve styling of utility for better readability. at 2024-11-01 17:41:43
* Commit 4: Docs: Fix bug in UI for better maintainability. at 2024-11-04 17:15:19
* Commit 5: Style: Clean up workflow to improve user experience. at 2024-11-04 17:34:09
* Commit 6: Chore: Optimize performance of dependencies for better readability. at 2024-11-04 10:38:01
* Commit 7: Build: Refactor code in utility for faster execution. at 2024-11-04 12:21:24
* Commit 8: Feat: Refactor code in API to support new requirements. at 2024-11-05 09:09:31
