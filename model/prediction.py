# @author lmiguelmh
# @since 

import codecs
import datetime
import pickle

import numpy as np
import pandas
from sklearn.externals import joblib
from sklearn.svm import SVR

pkz_file = '../data/sentiment/all.pkz'
with open(pkz_file, 'rb') as f:
    compressed_content = f.read()
sentiment = pickle.loads(codecs.decode(compressed_content, 'zlib_codec'))

sentiment_df = pandas.DataFrame(
    [[v['Verynegative'] if 'Verynegative' in v else 0,
      v['Negative'] if 'Negative' in v else 0,
      v['Neutral'] if 'Neutral' in v else 0,
      v['Positive'] if 'Positive' in v else 0,
      v['Verypositive'] if 'Verypositive' in v else 0] for k, v in sentiment.items()],
    columns=['Verynegative', 'Negative', 'Neutral', 'Positive', 'Verypositive'],
    index=[datetime.datetime.strptime(k, '%Y%m%d').date() for k in sentiment.keys()]
)
sentiment_df = sentiment_df.sort_index(ascending=True)
# df.head()

file = '../data/bitcoin/market-price.blockchain.info.csv'
df = pandas.read_csv(file,
                     header=None,
                     names=['Date', 'Close Price'],
                     index_col='Date',
                     parse_dates=True,
                     na_values=['nan'])

# select only some dates using an index and an inner join
dates = pandas.date_range('2016/10/01', '2016/10/31')
selected_df = pandas.DataFrame(index=dates)
selected_df = selected_df.join(df)  # join prices
selected_df = selected_df.join(sentiment_df)  # join sentiment
selected_df.head()

# no es necesario los dìas
# podemos probar con las noticias de 1 dìa antes o del mismo dìa
# dts = selected_df.index.values.astype(datetime.datetime) / 1e9
# X:
# [
# sample1: [feature1 feature2 feature3 ...]
# sample2: [feature1 feature2 feature3 ...]
# ...
# ]
# X = selected_df.values
X = selected_df[['Verynegative', 'Negative', 'Neutral', 'Positive', 'Verypositive']].values
y = np.asarray(selected_df['Close Price'])
print(X.shape)
print(y.shape)
# print("X %d items" % len(X))
# print("y %d items" % len(y))

clf_lin = SVR(kernel='linear', C=1e3, verbose=True)
clf_poly = SVR(kernel='poly', C=1e3, degree=2, verbose=False)
clf_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1, verbose=True)

# print('start svr linear fitting ' + str(datetime.datetime.now()))
# clf_lin.fit(X, y)
# joblib.dump(clf_lin, '../data/model/sentiment_lin.pkl')
# print('end svr linear fitting ' + str(datetime.datetime.now()))

print('start svr poly fitting ' + str(datetime.datetime.now()))
clf_poly.fit(X, y)
joblib.dump(clf_poly, '../data/model/sentiment_poly.pkl')
print('end svr poly fitting ' + str(datetime.datetime.now()))

# print('start svr rbf fitting ' + str(datetime.datetime.now()))
# clf_rbf.fit(X, y)
# joblib.dump(clf_rbf, '../data/model/sentiment_rbf.pkl')
# print('end svr rbf fitting ' + str(datetime.datetime.now()))

# plt.scatter(X, y, color='black', label='Data')  # plotting the initial datapoints
# plt.plot(X, clf_lin.predict(X), color='red', label='lin model')
# plt.plot(X, clf_poly.predict(X), color='blue', label='poly model')
# plt.plot(X, clf_rbf.predict(X), color='green', label='rbf model')
# plt.xlabel('Date')
# plt.ylabel('Price')
# plt.title('Support Vector Regression')
# plt.legend(loc='upper left')
# plt.show()
