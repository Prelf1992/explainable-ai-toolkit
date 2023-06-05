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

# Simulated change for commit 12 on 2023-01-23 15:23:14

# Simulated change for commit 15 on 2023-01-25 14:07:23

# Simulated change for commit 16 on 2023-01-26 16:49:31

# Simulated change for commit 18 on 2023-01-27 15:54:34

# Simulated change for commit 23 on 2023-02-02 12:16:25

# Simulated change for commit 24 on 2023-02-02 10:24:33

# Simulated change for commit 25 on 2023-02-02 10:05:50

# Simulated change for commit 29 on 2023-02-10 12:38:39

# Simulated change for commit 34 on 2023-02-15 16:22:06

# Simulated change for commit 35 on 2023-02-17 17:00:23

# Simulated change for commit 39 on 2023-02-20 13:42:04

# Simulated change for commit 41 on 2023-02-23 16:51:56

# Simulated change for commit 42 on 2023-02-23 14:55:28

# Simulated change for commit 43 on 2023-02-28 11:49:18

# Simulated change for commit 46 on 2023-03-02 13:43:46

# Simulated change for commit 47 on 2023-03-03 16:36:04

# Simulated change for commit 51 on 2023-03-07 12:23:57

# Simulated change for commit 53 on 2023-03-09 17:27:01

# Simulated change for commit 56 on 2023-03-14 16:03:54

# Simulated change for commit 57 on 2023-03-14 11:05:24

# Simulated change for commit 59 on 2023-03-21 09:46:17

# Simulated change for commit 60 on 2023-03-21 17:32:23

# Simulated change for commit 61 on 2023-03-22 16:33:01

# Simulated change for commit 64 on 2023-04-04 15:04:01

# Simulated change for commit 66 on 2023-04-06 14:32:12

# Simulated change for commit 67 on 2023-04-07 17:14:21

# Simulated change for commit 68 on 2023-04-10 16:21:26

# Simulated change for commit 69 on 2023-04-11 17:20:12

# Simulated change for commit 70 on 2023-04-11 10:53:03

# Simulated change for commit 71 on 2023-04-13 13:15:43

# Simulated change for commit 73 on 2023-04-14 14:49:31

# Simulated change for commit 76 on 2023-04-20 12:04:55

# Simulated change for commit 77 on 2023-04-20 09:54:06

# Simulated change for commit 79 on 2023-04-25 13:48:37

# Simulated change for commit 84 on 2023-05-04 16:18:21

# Simulated change for commit 87 on 2023-05-08 12:08:55

# Simulated change for commit 89 on 2023-05-10 17:50:01

# Simulated change for commit 90 on 2023-05-10 16:57:06

# Simulated change for commit 91 on 2023-05-10 12:40:43

# Simulated change for commit 93 on 2023-05-16 14:20:38

# Simulated change for commit 94 on 2023-05-17 14:03:52

# Simulated change for commit 95 on 2023-05-17 09:54:32

# Simulated change for commit 96 on 2023-05-17 13:13:50

# Simulated change for commit 99 on 2023-05-24 17:41:17

# Simulated change for commit 104 on 2023-05-25 12:27:07

# Simulated change for commit 105 on 2023-05-26 11:39:20

# Simulated change for commit 108 on 2023-05-29 13:48:46

# Simulated change for commit 110 on 2023-05-30 16:57:38

# Simulated change for commit 111 on 2023-05-31 11:49:09

# Simulated change for commit 115 on 2023-06-05 09:23:34
