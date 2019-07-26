import argparse
import pandas as pd
import plotly
import pickle
import plotly.graph_objs as go
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support,classification_report
from sklearn.preprocessing import label_binarize


def main(infile_input, infile_output, outfile):
    """
    Produce an interactive confusion matrix (heatmap), precision, recall, fscore
    Args:
        infile_input: str, input tabular file with true labels
        infile_output: str, input tabular file with predicted labels
    """
    
    df_input = pd.read_csv(infile_input, sep='\t', parse_dates=True)
    df_output = pd.read_csv(infile_output, sep='\t', parse_dates=True)
    true_labels = df_input.iloc[:, -1].copy()
    predicted_labels = df_output.iloc[:, -1].copy()
    axis_labels = list(set(true_labels))
    c_matrix = confusion_matrix(true_labels, predicted_labels)

    #print(classification_report(true_labels, predicted_labels))
    #print("Confusion matrix:\n\n",c_matrix)

    f = open(outfile, "w")
    f.write(classification_report(true_labels, predicted_labels))
    f.write("\n")
    f.write("Confusion Matrix:\n\n")
    f.write(str(c_matrix))
    f.close()

    print(c_matrix)
    '''
    data = [
        go.Heatmap(
            z=c_matrix,
            x=axis_labels,
            y=axis_labels,
            colorscale='Portland',
        )
    ]

    layout = go.Layout(
        title='Confusion Matrix between true and predicted class labels',
        xaxis=dict(title='Predicted class labels'),
        yaxis=dict(title='True class labels')
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename="output_confusion.html", auto_open=False)

    # plot precision, recall and f_score for each class label
    precision, recall, f_score, _ = precision_recall_fscore_support(true_labels, predicted_labels)

    trace_precision = go.Scatter(
        x=axis_labels,
        y=precision,
        mode='lines+markers',
        name='Precision'
    )

    trace_recall = go.Scatter(
        x=axis_labels,
        y=recall,
        mode='lines+markers',
        name='Recall'
    )

    trace_fscore = go.Scatter(
        x=axis_labels,
        y=f_score,
        mode='lines+markers',
        name='F-score'
    )

    layout_prf = go.Layout(
        title='Precision, recall and f-score of true and predicted class labels',
        xaxis=dict(title='Class labels'),
        yaxis=dict(title='Precision, recall and f-score')
    )

    data_prf = [trace_precision, trace_recall, trace_fscore]
    fig_prf = go.Figure(data=data_prf, layout=layout_prf)
    plotly.offline.plot(fig_prf, filename="output_prf.html", auto_open=False)
    '''

if __name__ == "__main__":
    aparser = argparse.ArgumentParser()
    aparser.add_argument("-t", "--true", dest="infile_true", required=True)
    aparser.add_argument("-p", "--predicted", dest="infile_predicted", required=True)
    aparser.add_argument("-o", "--output", dest="outfile", required=True)
    args = aparser.parse_args()
    main(args.infile_true, args.infile_predicted,args.outfile)


