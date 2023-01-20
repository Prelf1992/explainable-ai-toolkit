import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import lime
import lime.lime_tabular
import shap
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format=\'%(asctime)s - %(levelname)s - %(message)s\')

class ExplainableAIToolkit:
    """
    A toolkit for generating explanations for machine learning model predictions.
    Supports LIME and SHAP for tabular data.
    """

    def __init__(self, model, feature_names: list, class_names: list):
        """
        Initializes the ExplainableAIToolkit.

        Args:
            model: The trained machine learning model (e.g., scikit-learn classifier).
            feature_names (list): List of feature names used by the model.
            class_names (list): List of class names for classification tasks.
        """
        self.model = model
        self.feature_names = feature_names
        self.class_names = class_names
        logging.info("ExplainableAIToolkit initialized.")

    def _predict_proba_wrapper(self, data):
        """
        Wrapper function for model.predict_proba to be compatible with LIME.
        """
        return self.model.predict_proba(data)

    def explain_with_lime(self, instance: np.ndarray, num_features: int = 5) -> lime.explanation.Explanation:
        """
        Generates a LIME explanation for a single instance.

        Args:
            instance (np.ndarray): The instance to explain.
            num_features (int): The number of features to include in the explanation.

        Returns:
            lime.explanation.Explanation: A LIME explanation object.
        """
        logging.info(f"Generating LIME explanation for instance: {instance[:5]}...")
        explainer = lime.lime_tabular.LimeTabularExplainer(
            training_data=np.array([instance]), # LIME expects training data for background
            feature_names=self.feature_names,
            class_names=self.class_names,
            mode=\'classification\'
        )
        explanation = explainer.explain_instance(
            data_row=instance,
            predict_fn=self._predict_proba_wrapper,
            num_features=num_features
        )
        logging.info("LIME explanation generated.")
        return explanation

    def explain_with_shap(self, X_train: pd.DataFrame, instance: np.ndarray) -> np.ndarray:
        """
        Generates a SHAP explanation for a single instance.

        Args:
            X_train (pd.DataFrame): Training data used to fit the model (for background distribution).
            instance (np.ndarray): The instance to explain.

        Returns:
            np.ndarray: SHAP values for the instance.
        """
        logging.info(f"Generating SHAP explanation for instance: {instance[:5]}...")
        explainer = shap.TreeExplainer(self.model, X_train)
        shap_values = explainer.shap_values(instance)
        logging.info("SHAP explanation generated.")
        return shap_values

    def print_lime_explanation(self, explanation: lime.explanation.Explanation):
        """
        Prints a formatted LIME explanation.
        """
        logging.info("Printing LIME explanation:")
        for feature, weight in explanation.as_list():
            print(f"  {feature}: {weight:.4f}")

    def print_shap_explanation(self, shap_values: np.ndarray, instance: np.ndarray):
        """
        Prints a formatted SHAP explanation.
        """
        logging.info("Printing SHAP explanation:")
        # For multi-class, shap_values is a list of arrays
        if isinstance(shap_values, list):
            for i, class_shap_values in enumerate(shap_values):
                print(f"  Class {self.class_names[i]} SHAP values:")
                for j, feature_name in enumerate(self.feature_names):
                    print(f"    {feature_name}: {class_shap_values[j]:.4f}")
        else:
            for i, feature_name in enumerate(self.feature_names):
                print(f"  {feature_name}: {shap_values[i]:.4f}")


if __name__ == "__main__":
    # 1. Generate synthetic data
    np.random.seed(42)
    data_size = 1000
    features = {
        'age': np.random.randint(18, 70, data_size),
        'income': np.random.normal(50000, 15000, data_size),
        'education_years': np.random.randint(8, 20, data_size),
        'loan_amount': np.random.normal(10000, 5000, data_size)
    }
    X = pd.DataFrame(features)
    # Create a binary target variable based on a simple rule with some noise
    y = ((X['income'] > 55000) & (X['education_years'] > 12) | (X['loan_amount'] < 7000)).astype(int)
    y = y ^ np.random.randint(0, 2, data_size) # Add some noise

    feature_names = list(X.columns)
    class_names = ['No Loan Default', 'Loan Default']

    # 2. Train a simple RandomForestClassifier model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logging.info(f"Model accuracy: {accuracy:.4f}")

    # 3. Initialize the ExplainableAIToolkit
    xai_toolkit = ExplainableAIToolkit(model, feature_names, class_names)

    # 4. Select an instance to explain
    instance_to_explain = X_test.iloc[0].values
    logging.info(f"\nExplaining instance: {X_test.iloc[0].to_dict()}")

    # 5. Generate and print LIME explanation
    lime_explanation = xai_toolkit.explain_with_lime(instance_to_explain)
    xai_toolkit.print_lime_explanation(lime_explanation)

    # 6. Generate and print SHAP explanation
    shap_values = xai_toolkit.explain_with_shap(X_train, instance_to_explain)
    xai_toolkit.print_shap_explanation(shap_values, instance_to_explain)

    logging.info("\nDemonstration of ExplainableAIToolkit complete.")

# Simulated change for commit 6 on 2023-01-13 12:22:36

# Simulated change for commit 7 on 2023-01-16 13:57:23

# Simulated change for commit 9 on 2023-01-18 13:01:03

# Simulated change for commit 11 on 2023-01-20 11:22:09
