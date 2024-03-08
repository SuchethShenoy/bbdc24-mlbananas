import numpy as np
import pandas as pd

class MulticlassPrecisionRecall():
    
    def __init__(self) -> None:
        pass

    def get_multiclass_evaluation(self, y_test, y_pred):
        y_pred = np.array(y_pred)
        y_test = np.array(y_test)
        y_test_categories = np.unique(y_pred)
        y_pred_categories = np.unique(y_test)
        all_categories = np.unique(np.concatenate((y_test_categories,y_pred_categories)))
        true_positive = {}
        false_positive = {}
        false_negative = {}
        precision = {}
        recall = {}
        for category in all_categories:
            true_positive[category] = 0
            false_positive[category] = 0
            false_negative[category] = 0
            precision[category] = 0
            recall[category] = 0
        for i in range(len(y_pred)):
            if y_pred[i]==y_test[i]:
                true_positive[y_pred[i]]+=1
            elif y_pred[i]!=y_test[i]:
                false_positive[y_pred[i]]+=1
                false_negative[y_test[i]]+=1
        
        for category in all_categories:
            try:
                precision[category] = true_positive[category]/(true_positive[category]+false_positive[category])
            except:
                precision[category] = np.nan
            try:
                recall[category] = true_positive[category]/(true_positive[category]+false_negative[category])
            except:
                recall[category] = np.nan
        
        return pd.DataFrame({
            "precision":precision, 
            "recall":recall,
            "true_positive":true_positive,
            "false_positive" :false_positive,
            "false_negative":false_negative}).T