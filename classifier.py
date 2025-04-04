from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
import os

class NoteClassifier:
    def __init__(self):
        self.categories = [
            "Finance", "Health", "Work", "Travel", 
            "Technology", "Personal", "Education", "Other"
        ]
        self.model_path = "models/classifier.joblib"
        self._initialize_model()

    def _initialize_model(self):
        if os.path.exists(self.model_path):
            self.pipeline = joblib.load(self.model_path)
        else:
            self._train_new_model()

    def _train_new_model(self):
        # Training data for each category
        training_data = {
            "Finance": [
                "budget investment stocks money finance banking",
                "expenses income tax savings portfolio",
                "mortgage loan credit card payment"
            ],
            "Health": [
                "doctor medicine health fitness exercise",
                "diet nutrition wellness medical checkup",
                "symptoms treatment prescription vitamins"
            ],
            "Work": [
                "meeting project deadline presentation",
                "report schedule conference call",
                "task assignment progress update"
            ],
            "Travel": [
                "flight hotel vacation beach trip",
                "itinerary booking destination sightseeing",
                "passport visa accommodation tour"
            ],
            "Technology": [
                "software development code programming",
                "system update bug fix deployment",
                "network security database server"
            ],
            "Personal": [
                "family friends birthday celebration",
                "hobby interest personal goal",
                "shopping gift wishlist"
            ],
            "Education": [
                "study course homework assignment",
                "exam preparation research thesis",
                "learning training workshop seminar"
            ]
        }

        # Prepare training data
        X = []
        y = []
        for category, texts in training_data.items():
            X.extend(texts)
            y.extend([category] * len(texts))

        # Create and train pipeline
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=1000,
                ngram_range=(1, 2),
                stop_words='english'
            )),
            ('clf', MultinomialNB())
        ])
        
        self.pipeline.fit(X, y)
        
        # Save the model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.pipeline, self.model_path)

    def classify(self, text: str) -> str:
        """
        Classify the given text into one of the predefined categories.
        
        Args:
            text (str): The text to classify
            
        Returns:
            str: The predicted category
        """
        prediction = self.pipeline.predict([text])[0]
        return prediction

    def get_probabilities(self, text: str) -> dict:
        """
        Get probability scores for all categories.
        
        Args:
            text (str): The text to classify
            
        Returns:
            dict: Probability scores for each category
        """
        probs = self.pipeline.predict_proba([text])[0]
        return dict(zip(self.categories, probs)) 