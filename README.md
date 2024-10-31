<a href="https://www.albertschool.com/"><img src = "https://global-uploads.webflow.com/6273671ff5e4fa1d7730ca1c/6324975eae5b3c2d24a79022_logo_bleu1080x170_svg.svg" width = 200></a>

<br><br>

<h1 align=center>YouTube Spam Detection</h1>
<h3 align=center>ML for Business II</h3>

<br>

<p align=center> Elie LAFORGE, Yunan WANG <p align=center> Albert School - 2024

<br><br>

## 1. Context and Business Need

In the ever-growing landscape of YouTube, comment sections often become breeding grounds for spam, reducing the quality of user interactions and potentially harming content creators' engagement metrics. There's a pressing need for an efficient, automated system to detect and flag spam comments, enhancing the overall user experience and maintaining the integrity of discussions on the platform.

## 2. Dataset

We utilized two datasets from Kaggle for training our spam detection model:

1. [YouTube Comments Spam Dataset](https://www.kaggle.com/datasets/ahsenwaheed/youtube-comments-spam-dataset)
2. [5000 YouTube Spam/Not-Spam Dataset](https://www.kaggle.com/datasets/madhuragl/5000-youtube-spamnot-spam-dataset)

These datasets contain labeled YouTube comments, with features including comment_id, author, date, content, and video name. The target variable is the 'CLASS' column, where 1 indicates spam and 0 indicates non-spam.

## 3. Baseline Model

Our baseline approach included:

- Features: TF-IDF vectorization of comment content
- Preprocessing: Data cleaning, handling missing values, and removing duplicates
- Validation Strategy: 80-20 train-test split
- Model: Logistic Regression
- Metrics: Accuracy, Precision, Recall, F1 Score, and ROC-AUC

## 4. Model Iteration and Improvement

We iterated on our baseline model by:

1. Experimenting with different algorithms:
   - Bernoulli Naive Bayes
   - XGBoost (final choice)

2. Feature engineering:
   - Advanced text preprocessing techniques
   - Exploring additional metadata features

3. Hyperparameter tuning for XGBoost:
   - learning rate = 0.2
   - max depth = 6
   - n estimators = 150

The final XGBoost model achieved significant improvements:
- F1 Score (using threshold 0.65): 0.8656
- ROC-AUC Score: 0.9570
- Train Accuracy: 0.9502
- Test Accuracy (using threshold 0.65): 0.9047

## 5. Proposed Solution and Methodologies

Our project aims to develop a robust YouTube Spam Detection system using machine learning techniques. The end product is a Chrome extension that seamlessly integrates with YouTube's interface, providing real-time spam probability scores for comments.

Key methodologies include:
- Data preprocessing and feature engineering on YouTube comment datasets
- Implementing and training an XGBoost classifier for spam detection
- Developing a FastAPI backend to serve the trained model
- Creating a Chrome extension for real-time comment analysis on YouTube pages

## 6. Project Architecture

The project is structured as follows:

- `src/spam_detector/`: Core Python package
  - `models/`: Contains model training scripts and saved models
  - `services/`: Business logic and API integration
  - `interfaces/`: Data models and type definitions
  - `app.py`: FastAPI application entry point
- `notebooks/`: Jupyter notebooks for EDA and model development
- `tests/`: Pytest test suite
- `chrome-extension/`: Chrome extension source code
- `.github/workflows/`: CI/CD pipeline configurations
- `Dockerfile`: Docker configuration for containerization
- `heroku.yml`: Heroku deployment configuration

## 7. Features

- Machine learning-based spam detection using XGBoost
- Real-time comment analysis through a Chrome extension
- FastAPI backend for efficient model serving
- Comprehensive test suite using pytest
- Continuous Integration and Continuous Deployment (CI/CD) with GitHub Actions
- Docker support for containerization and easy deployment
- Heroku deployment for scalable hosting
- MLflow integration for experiment tracking and model versioning
- Experiment tracking and model versioning with MLflow
- Comprehensive EDA and model development process documented in Jupyter notebooks

## 8. Development and Deployment

- Containerization with Docker for consistent environments
- CI/CD pipeline using GitHub Actions for automated testing and deployment
- Heroku deployment for scalable hosting of the backend API
- Chrome extension for seamless integration with YouTube's interface

## 9. Future Improvements

- Implement deep learning models (e.g., LSTM, BERT) for potentially better performance
- Expand feature engineering efforts
- Collect and incorporate a larger, more diverse dataset for improved generalization

## 10. Credits

- [YouTube Data API](https://developers.google.com/youtube/v3/docs)
- Training datasets
  - [YouTube Comments Spam Dataset](https://www.kaggle.com/datasets/ahsenwaheed/youtube-comments-spam-dataset)
  - [5000 YouTube Spam/Not-Spam Dataset](https://www.kaggle.com/datasets/madhuragl/5000-youtube-spamnot-spam-dataset)

## 11. Notice

- You may find the `eda.ipynb` notebook in the `notebooks/` folder, due to project structure constraints.
- You may find the `scripts.py` file in the `src/spam_detector/models/train_model.py`, due to project structure constraints.
- For API server documentation, please access to `localhost:8000/docs` once launching the API dev server.