import pandas as pd
import numpy as np
import plotly
from matplotlib import pyplot as plt
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

import warnings

warnings.filterwarnings("ignore")


def iForest(df, plot = True):
    """
        df header : timestamp   value
        timestamp format: "%Y-%m-%d %H:%M:%S"
    """

    from sklearn.ensemble import IsolationForest
    # to_model_column='value'
    clf = IsolationForest(n_estimators=10, max_samples='auto', contamination='auto', max_features=1.0, bootstrap=False,
                          n_jobs=-1, random_state=42, verbose=0, behaviour='new')
    clf.fit(df[['value']])
    df['scores'] = clf.decision_function(df[['value']])
    df['anomaly'] = clf.predict(df[['value']])
    df.head()
    df.loc[df['anomaly'] == 1, 'anomaly'] = 0
    df.loc[df['anomaly'] == -1, 'anomaly'] = 1
    pd.value_counts(df.values.flatten())

    # Now lets start fitting this to an isolation forest model with contamination parameter set as 4% based on my intuition from the visualization.

    def plot_anomaly(df, metric_name):
        df.timestamp = pd.to_datetime(df['timestamp'].astype(str), format="%Y-%m-%d %H:%M:%S")
        dates = df.timestamp
        # identify the anomaly points and create a array of its values for plot
        bool_array = (abs(df['anomaly']) > 0)
        actuals = df["value"][-len(bool_array):]
        anomaly_points = bool_array * actuals
        anomaly_points[anomaly_points == 0] = np.nan
        # A dictionary for conditional format table based on anomaly
        color_map = {0: "'rgba(228, 222, 249, 0.65)'", 1: "red"}
        # Table which includes Date,Actuals,Change occured from previous point
        table = go.Table(
            domain=dict(x=[0, 1],
                        y=[0, 0.3]),
            columnwidth=[1, 2],
            # columnorder=[0, 1, 2,],
            header=dict(height=20,
                        values=[['<b>Date</b>'], ['<b>Actual Values </b>'],
                                ],
                        font=dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                        fill=dict(color='#d562be')),
            cells=dict(values=[df.round(3)[k].tolist() for k in ['timestamp', 'value']],
                       row=dict(color='#506784'),
                       align=['center'] * 5,
                       font=dict(color=['rgb(40, 40, 40)'] * 5, size=12),
                       # format = [None] + [",.4f"] + [',.4f'],
                       # suffix=[None] * 4,
                       suffix=[None] + [''] + [''] + ['%'] + [''],
                       height=27,
                       fill=dict(color=[df['anomaly'].map(color_map)],  # map based on anomaly level from dictionary
                                 )
                       ))
        # Plot the actuals points
        Actuals = go.Scatter(name='Actuals',
                             x=dates,
                             y=df['value'],
                             xaxis='x1', yaxis='y1',
                             mode='row',
                             marker=dict(size=12,
                                         row=dict(width=1),
                                         color="blue"))
        # Highlight the anomaly points
        anomalies_map = go.Scatter(name="Anomaly",
                                   showlegend=True,
                                   x=dates,
                                   y=anomaly_points,
                                   mode='markers',
                                   xaxis='x1',
                                   yaxis='y1',
                                   marker=dict(color="red",
                                               size=11,
                                               row=dict(
                                                   color="red",
                                                   width=2)))
        axis = dict(
            showline=True,
            zeroline=False,
            showgrid=True,
            mirror=True,
            ticklen=4,
            gridcolor='#ffffff',
            tickfont=dict(size=10))
        layout = dict(
            width=1000,
            height=865,
            autosize=False,
            title=metric_name,
            margin=dict(t=75),
            showlegend=True,
            xaxis1=dict(axis, **dict(domain=[0, 1], anchor='y1', showticklabels=True)),
            yaxis1=dict(axis, **dict(domain=[2 * 0.21 + 0.20, 1], anchor='x1', hoverformat='.2f')))
        fig = go.Figure(data=[table, anomalies_map, Actuals], layout=layout)
        plotly.offline.plot(fig, filename="output_iforest/" + metric_name)

        # iplot(fig)
        # pyplot.show()

    # In[25]:

    if plot: plot_anomaly(df, 'anomalies')

    # In[26]:

    ano_before = (len(df.loc[df['anomaly'] == 1]) / len(df)) * 100

    # print("Percentage of anomalies in data: {:.2f}%".format(ano_before))

    # In[28]:

    df['scores'].hist()
    # plt.show()

    # In[29]:

    def iqr_bounds(scores, k=1.5):
        q1 = scores.quantile(0.25)
        q3 = scores.quantile(0.75)
        iqr = q3 - q1
        lower_bound = (q1 - k * iqr)
        upper_bound = (q3 + k * iqr)
        # print("Lower bound:{} \nUpper bound:{}".format(lower_bound, upper_bound))
        return lower_bound, upper_bound

    lower_bound, upper_bound = iqr_bounds(df['scores'], k=2)

    # In[30]:

    df['anomaly'] = 0
    df['anomaly'] = (df['scores'] < lower_bound) | (df['scores'] > upper_bound)
    df['anomaly'] = df['anomaly'].astype(int)
    # print(df.head())
    if plot: plot_anomaly(df, 'iqr based')

    ano_after = (len(df.loc[df['anomaly'] == 1]) / len(df)) * 100

    print("Percentage of anomalies in data: {:.2f}, filtered: {:.2f}%".format(ano_before, ano_after))
    return ano_before, ano_after


def preview_data_iforest(df):
    # full_df = pd.read_csv('ec2_cpu_utilization_5f5533.csv')
    df.head()
    print(df['timestamp'].min())
    print(df['timestamp'].max())
    print(len(df['timestamp']))

    # Using graph_objects
    init_notebook_mode(connected=True)
    import plotly.graph_objs as go
    fig = go.Figure(data=[go.Scatter(x=df['timestamp'], y=df['value'])])
    iplot(fig)
    plotly.offline.plot(fig, filename='output_iforest/full_data.html')


def main():
    dataset_name = 'ec21ts.csv'
    # create output directory
    from pathlib import Path
    Path("output_iforest").mkdir(parents=True, exist_ok=True)

    full_df = pd.read_csv('../../datasets/' + dataset_name)
    full_df.reset_index()
    full_df["timestamp"] = pd.Series(pd.date_range('2018-04-09', periods=len(full_df), freq='1D20min')).dt.strftime(
        "%Y-%m-%d %H:%M:%S")
    # print(full_df.head())
    # preview_data_iforest(full_df)
    ano_before, ano_after = iForest(full_df)
    print("Percentage of anomalies in data: {:.2f}%".format(ano_after))


if __name__ == "__main__":
    main()
