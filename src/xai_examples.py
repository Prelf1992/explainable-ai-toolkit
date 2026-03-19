
import lime
import lime.lime_tabular
import shap
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt

def run_xai_example():
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
    print("LIME Explanation for instance 0:")
    # explanation_lime.show_in_note() # This would open a browser, not suitable for sandbox
    print(explanation_lime.as_list())

    # SHAP Explainer
    explainer_shap = shap.TreeExplainer(model)
    shap_values = explainer_shap.shap_values(X)
    print("
SHAP Explanation (first instance for class 1):
", shap_values[1][0])

    # shap.summary_plot(shap_values, X, feature_names=[f'feature_{i}' for i in range(X.shape[1])])
    # plt.show() # This would open a plot, not suitable for sandbox

if __name__ == "__main__":
    run_xai_example()
