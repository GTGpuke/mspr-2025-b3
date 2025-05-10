from src.preprocess import load_and_prepare_data
from src.model import build_model, train_model
from src.evaluate import evaluate_model

# 1. Charger et préparer les données
X_train, X_test, y_train, y_test = load_and_prepare_data("data/elections.csv")

# 2. Créer le modèle
model = build_model(input_shape=X_train.shape[1])

# 3. Entraîner le modèle
history = train_model(model, X_train, y_train)

# 4. Évaluer le modèle
evaluate_model(model, X_test, y_test)
