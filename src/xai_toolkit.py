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

# Simulated change for commit 116 on 2023-06-05 09:38:24

# Simulated change for commit 118 on 2023-06-06 15:45:11

# Simulated change for commit 120 on 2023-06-07 14:46:09

# Simulated change for commit 122 on 2023-06-12 16:41:03

# Simulated change for commit 124 on 2023-06-14 09:32:33

# Simulated change for commit 126 on 2023-06-15 12:17:19

# Simulated change for commit 129 on 2023-06-22 14:33:51

# Simulated change for commit 130 on 2023-06-22 16:55:37

# Simulated change for commit 131 on 2023-06-22 13:07:00

# Simulated change for commit 133 on 2023-06-30 16:52:56

# Simulated change for commit 134 on 2023-07-03 17:22:00

# Simulated change for commit 135 on 2023-07-06 11:22:05

# Simulated change for commit 137 on 2023-07-12 13:17:05

# Simulated change for commit 139 on 2023-07-17 16:46:08

# Simulated change for commit 141 on 2023-07-19 10:48:20

# Simulated change for commit 142 on 2023-07-20 16:41:20

# Simulated change for commit 143 on 2023-07-20 16:01:31

# Simulated change for commit 145 on 2023-07-27 15:47:06

# Simulated change for commit 146 on 2023-07-28 12:32:27

# Simulated change for commit 147 on 2023-07-28 11:17:11

# Simulated change for commit 149 on 2023-07-31 13:50:12

# Simulated change for commit 151 on 2023-07-31 10:10:34

# Simulated change for commit 152 on 2023-08-01 13:09:06

# Simulated change for commit 154 on 2023-08-02 15:15:49

# Simulated change for commit 155 on 2023-08-03 10:41:00

# Simulated change for commit 158 on 2023-08-09 15:26:26

# Simulated change for commit 159 on 2023-08-09 17:54:25

# Simulated change for commit 161 on 2023-08-14 15:19:11

# Simulated change for commit 162 on 2023-08-14 15:39:59

# Simulated change for commit 163 on 2023-08-21 14:40:57

# Simulated change for commit 164 on 2023-08-21 13:41:31

# Simulated change for commit 167 on 2023-08-29 16:16:37

# Simulated change for commit 169 on 2023-08-31 09:41:39

# Simulated change for commit 170 on 2023-08-31 09:04:46

# Simulated change for commit 171 on 2023-09-01 11:28:12

# Simulated change for commit 173 on 2023-09-05 10:35:18

# Simulated change for commit 174 on 2023-09-07 15:40:04

# Simulated change for commit 175 on 2023-09-07 14:49:31

# Simulated change for commit 178 on 2023-09-08 09:44:12

# Simulated change for commit 180 on 2023-09-11 17:30:14

# Simulated change for commit 184 on 2023-09-25 16:14:33

# Simulated change for commit 186 on 2023-09-27 17:14:57

# Simulated change for commit 189 on 2023-10-02 12:44:46

# Simulated change for commit 190 on 2023-10-02 15:04:51

# Simulated change for commit 192 on 2023-10-04 10:53:02

# Simulated change for commit 196 on 2023-10-06 16:36:43

# Simulated change for commit 199 on 2023-10-11 13:34:35

# Simulated change for commit 201 on 2023-10-19 16:34:04

# Simulated change for commit 203 on 2023-10-23 14:30:54

# Simulated change for commit 204 on 2023-10-23 13:31:06

# Simulated change for commit 205 on 2023-10-24 13:36:12

# Simulated change for commit 209 on 2023-10-30 12:12:10

# Simulated change for commit 212 on 2023-11-01 10:54:23

# Simulated change for commit 213 on 2023-11-01 13:14:39

# Simulated change for commit 215 on 2023-11-07 15:17:35

# Simulated change for commit 217 on 2023-11-07 11:37:35

# Simulated change for commit 219 on 2023-11-09 10:50:03

# Simulated change for commit 220 on 2023-11-14 15:05:58

# Simulated change for commit 221 on 2023-11-15 16:36:25

# Simulated change for commit 225 on 2023-11-20 14:16:53

# Simulated change for commit 226 on 2023-11-23 13:19:41

# Simulated change for commit 227 on 2023-11-24 17:28:37

# Simulated change for commit 230 on 2023-11-27 10:44:58

# Simulated change for commit 231 on 2023-11-27 16:56:20

# Simulated change for commit 232 on 2023-11-28 16:23:00

# Simulated change for commit 233 on 2023-11-29 11:25:46

# Simulated change for commit 236 on 2023-12-01 17:07:40

# Simulated change for commit 238 on 2023-12-05 11:21:34

# Simulated change for commit 240 on 2023-12-13 09:13:24

# Simulated change for commit 242 on 2023-12-15 09:58:27

# Simulated change for commit 243 on 2023-12-18 15:44:35

# Simulated change for commit 247 on 2023-12-27 16:37:53

# Simulated change for commit 248 on 2023-12-29 16:26:43

# Simulated change for commit 249 on 2023-12-29 12:55:12

# Simulated change for commit 1 on 2024-01-01 16:59:49

# Simulated change for commit 6 on 2024-01-03 11:52:20

# Simulated change for commit 8 on 2024-01-05 16:16:19

# Simulated change for commit 9 on 2024-01-05 17:28:38

# Simulated change for commit 12 on 2024-01-12 16:24:14

# Simulated change for commit 14 on 2024-01-15 13:10:58

# Simulated change for commit 15 on 2024-01-15 14:45:21

# Simulated change for commit 17 on 2024-01-22 17:02:04

# Simulated change for commit 18 on 2024-01-24 14:10:19

# Simulated change for commit 20 on 2024-01-25 12:55:20

# Simulated change for commit 21 on 2024-01-25 15:20:12

# Simulated change for commit 22 on 2024-01-26 09:27:50

# Simulated change for commit 29 on 2024-02-07 14:39:51

# Simulated change for commit 30 on 2024-02-13 17:59:00

# Simulated change for commit 31 on 2024-02-13 17:59:38

# Simulated change for commit 34 on 2024-02-16 11:49:16

# Simulated change for commit 35 on 2024-02-19 13:12:06

# Simulated change for commit 38 on 2024-02-20 11:30:24

# Simulated change for commit 39 on 2024-02-21 12:27:59

# Simulated change for commit 42 on 2024-02-23 12:31:20

# Simulated change for commit 43 on 2024-02-23 12:32:16

# Simulated change for commit 49 on 2024-03-01 09:01:37

# Simulated change for commit 51 on 2024-03-06 17:31:21

# Simulated change for commit 54 on 2024-03-11 09:43:43

# Simulated change for commit 55 on 2024-03-11 09:17:45

# Simulated change for commit 59 on 2024-03-19 14:22:38

# Simulated change for commit 61 on 2024-03-21 11:44:43

# Simulated change for commit 65 on 2024-03-25 09:55:02

# Simulated change for commit 67 on 2024-03-25 16:10:12

# Simulated change for commit 70 on 2024-03-27 14:20:53

# Simulated change for commit 71 on 2024-03-28 12:02:07

# Simulated change for commit 74 on 2024-04-01 15:55:17

# Simulated change for commit 79 on 2024-04-04 17:47:19

# Simulated change for commit 80 on 2024-04-08 14:15:00

# Simulated change for commit 81 on 2024-04-08 13:54:58

# Simulated change for commit 83 on 2024-04-10 17:34:22

# Simulated change for commit 85 on 2024-04-11 16:15:40

# Simulated change for commit 87 on 2024-04-16 16:36:18

# Simulated change for commit 88 on 2024-04-23 17:01:28

# Simulated change for commit 89 on 2024-04-24 12:50:57

# Simulated change for commit 90 on 2024-04-24 16:40:03

# Simulated change for commit 91 on 2024-04-24 15:23:47

# Simulated change for commit 95 on 2024-05-01 12:46:30

# Simulated change for commit 97 on 2024-05-07 11:30:04

# Simulated change for commit 100 on 2024-05-13 16:35:16

# Simulated change for commit 101 on 2024-05-13 14:45:26

# Simulated change for commit 108 on 2024-05-20 17:34:54

# Simulated change for commit 110 on 2024-05-22 10:49:15

# Simulated change for commit 113 on 2024-05-28 15:31:38

# Simulated change for commit 116 on 2024-06-06 09:50:40

# Simulated change for commit 117 on 2024-06-07 10:58:57

# Simulated change for commit 120 on 2024-06-12 10:21:12

# Simulated change for commit 121 on 2024-06-13 10:10:33

# Simulated change for commit 123 on 2024-06-17 10:23:13

# Simulated change for commit 127 on 2024-06-26 11:43:32

# Simulated change for commit 128 on 2024-06-26 15:28:32

# Simulated change for commit 129 on 2024-06-27 13:18:55

# Simulated change for commit 130 on 2024-07-01 16:26:39

# Simulated change for commit 133 on 2024-07-03 14:38:03

# Simulated change for commit 134 on 2024-07-04 11:50:10

# Simulated change for commit 136 on 2024-07-05 15:55:21

# Simulated change for commit 142 on 2024-07-17 15:14:37

# Simulated change for commit 144 on 2024-07-18 11:54:13

# Simulated change for commit 145 on 2024-07-24 17:33:44

# Simulated change for commit 146 on 2024-07-24 14:15:59

# Simulated change for commit 147 on 2024-07-24 10:53:55

# Simulated change for commit 150 on 2024-08-05 16:14:09

# Simulated change for commit 152 on 2024-08-06 09:46:21

# Simulated change for commit 154 on 2024-08-08 10:03:45

# Simulated change for commit 155 on 2024-08-13 13:17:51

# Simulated change for commit 160 on 2024-08-22 16:25:16

# Simulated change for commit 162 on 2024-08-26 16:50:43

# Simulated change for commit 166 on 2024-09-12 11:09:43

# Simulated change for commit 168 on 2024-09-16 11:11:38

# Simulated change for commit 170 on 2024-09-19 17:37:04

# Simulated change for commit 171 on 2024-09-19 17:33:28

# Simulated change for commit 174 on 2024-09-23 13:02:35

# Simulated change for commit 176 on 2024-09-24 09:12:25

# Simulated change for commit 177 on 2024-09-26 10:51:19

# Simulated change for commit 181 on 2024-10-03 11:07:37

# Simulated change for commit 184 on 2024-10-08 11:03:08

# Simulated change for commit 185 on 2024-10-09 17:56:41

# Simulated change for commit 187 on 2024-10-11 16:28:09

# Simulated change for commit 188 on 2024-10-11 16:33:05

# Simulated change for commit 189 on 2024-10-14 16:40:13

# Simulated change for commit 196 on 2024-10-28 10:47:08

# Simulated change for commit 197 on 2024-10-29 09:49:14

# Simulated change for commit 198 on 2024-10-29 17:11:21

# Simulated change for commit 199 on 2024-10-30 16:40:43

# Simulated change for commit 200 on 2024-10-31 12:02:45

# Simulated change for commit 202 on 2024-11-04 12:52:10

# Simulated change for commit 203 on 2024-11-06 15:18:17

# Simulated change for commit 204 on 2024-11-06 16:20:10

# Simulated change for commit 211 on 2024-11-14 16:49:08

# Simulated change for commit 213 on 2024-11-18 15:39:16
