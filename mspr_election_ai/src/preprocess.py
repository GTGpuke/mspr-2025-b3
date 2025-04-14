import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_and_prepare_data(file_path):
    df = pd.read_csv(file_path)

    # Supposons que tu as une colonne 'resultat_election' (la cible)
    X = df.drop(columns=['resultat_election'])
    y = df['resultat_election']

    # Normalisation
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return train_test_split(X_scaled, y, test_size=0.2, random_state=42)
