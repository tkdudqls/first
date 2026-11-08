from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

texts = [
   "파이썬 데이터 추천", 
   "파이썬 데이터 분석",
   "파이썬 게임 게임 게임 게임 게임 게임 게임",
   "파이썬 게임 분석",
   "파이썬 데이터 추천"
]

v = TfidfVectorizer()
X = v.fit_transform(texts)
scores = cosine_similarity(X[0:1], X[1:]).flatten()
print(v.get_feature_names_out())
print(X.toarray().round(3))
print(scores.round(3))