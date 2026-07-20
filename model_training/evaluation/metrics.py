from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)


def calculate_metrics(y_true, y_pred):

    accuracy = accuracy_score(y_true, y_pred)

    report = classification_report(
        y_true,
        y_pred,
        digits=4
    )

    matrix = confusion_matrix(
        y_true,
        y_pred
    )

    return accuracy, report, matrix