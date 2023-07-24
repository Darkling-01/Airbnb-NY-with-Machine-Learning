from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from connection import sql_con
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


def cleaning():
    sql_query = sql_con()
    # dropping columns that we don't need
    sql_query = sql_query.drop(columns=['id', 'latitude', 'longitude', 'host_id',
                               'last_review', 'reviews_per_month', 'number_of_reviews', 'host_name',
                               'neighbourhood', 'room_type'], axis=1)

    return sql_query


# use neighbourhood_group (5 labels) and price for linear regression
def data_preprocessing():
    sql_query = cleaning()
    # label encoding
    label_encoder = preprocessing.LabelEncoder()
    # neighbourhood_group [0, 1, 2, 3]
    sql_query['neighbourhood_group'] = label_encoder.fit_transform(sql_query['neighbourhood_group'])
    sql_query.nunique()

    # scaling helps us for better results, predictions and accuracy
    # scaling/normalizing numerical features
    scalar = MinMaxScaler(feature_range=(50, 310))
    scaled_data = scalar.fit_transform(sql_query)
    scaled_sql = pd.DataFrame(scaled_data, columns=sql_query.columns)

    return scaled_sql


def data_split():
    # X is our independent variable, y is the target variable
    clean_dataset = data_preprocessing()
    X = clean_dataset.iloc[:, clean_dataset.columns != 'price']  # this method lets us pick the columns
    y = clean_dataset.iloc[:, clean_dataset.columns == 'price']  # target variable price
    #  training set is used to train the model
    #  testing set evaluates the model's performance
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # regression
    lin_reg = LinearRegression()
    lin_reg.fit(X_train, y_train)
    # before using the fit model we have to include predictions and evaluate
    y_pred = lin_reg.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print('MAE: %.3f' % mae)
    """
        OUTPUT:
        MAE: 20.976
    """