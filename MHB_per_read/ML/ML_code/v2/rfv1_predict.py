import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
import sys
import matplotlib.pyplot as plt
import pickle
import os.path
from sklearn.metrics import precision_score, recall_score, roc_auc_score, roc_curve
from sklearn.metrics import confusion_matrix
import itertools
from sklearn.metrics import plot_precision_recall_curve


modelfile=sys.argv[1]
testfile=sys.argv[2]

def plot_P_R_curve(poslabel):
    plot_precision_recall_curve(model, test, test_labels,pos_label=poslabel, name = 'rf')

def evaluate_model(predictions, probs):
    """Compare machine learning model to baseline performance.
    Computes statistics and shows ROC curve."""
    
    baseline = {}
    
    baseline['recall'] = recall_score(test_labels, 
                                     [1 for _ in range(len(test_labels))])
    baseline['precision'] = precision_score(test_labels, 
                                      [1 for _ in range(len(test_labels))])
    baseline['roc'] = 0.5
    
    results = {}
    
    results['recall'] = recall_score(test_labels, predictions)
    results['precision'] = precision_score(test_labels, predictions)
    results['roc'] = roc_auc_score(test_labels, probs)
    
   
    
    for metric in ['recall', 'precision', 'roc']:
        print(f'{metric.capitalize()} Baseline: {round(baseline[metric], 2)} Test: {round(results[metric], 2)}')
    
    # Calculate false positive rates and true positive rates
    base_fpr, base_tpr, _ = roc_curve(test_labels, [1 for _ in range(len(test_labels))])
    model_fpr, model_tpr, _ = roc_curve(test_labels, probs)

    plt.figure(figsize = (10, 8))
    plt.rcParams['font.size'] = 16
    
    # Plot both curves
    plt.plot(base_fpr, base_tpr, 'b', label = 'baseline')
    plt.plot(model_fpr, model_tpr, 'r', label = 'model')
    plt.legend();
    plt.xlabel('False Positive Rate'); 
    plt.ylabel('True Positive Rate'); plt.title('ROC Curves');

    mystr="AUC = "+str(round(results['roc'],2))
    plt.text(0.8, 0.2, mystr, fontsize=24)
    #plt.show();

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Oranges):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    Source: http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    # Plot the confusion matrix
    plt.figure(figsize = (14, 14))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title, size = 24)
    plt.colorbar(aspect=4)
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45, size = 24)
    plt.yticks(tick_marks, classes, size = 24)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    
    # Labeling the plot
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt), fontsize = 20,
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
        
    plt.grid(None)
    #plt.tight_layout()
    plt.subplots_adjust(left=0.15)
    plt.ylabel('True label', size = 24)
    plt.xlabel('Predicted label', size = 24)






outfileprefix=modelfile+"_testfile_"+os.path.basename(testfile)

with open(modelfile,'rb') as f:
    model=pickle.load(f)



f_names = model.feature_names









# Testing predictions (to determine performance)


df=pd.read_csv(testfile,sep="\t")


test=(df[f_names]).copy()






rf_predictions = model.predict(test)
rf_probs = model.predict_proba(test)[:, 1]

if 'label' in df.columns:
	test_labels=(df['label']).copy()




	# Plot formatting
	plt.style.use('fivethirtyeight')
	plt.rcParams['font.size'] = 18



	evaluate_model(rf_predictions, rf_probs)
	plt.savefig(outfileprefix+'_roc_auc_curve.png')






	# Confusion matrix

	cm = confusion_matrix(test_labels, rf_predictions)
	plot_confusion_matrix(cm, classes = ['positive', 'negative'],
	                      title = 'Confusion Matrix')

	plt.savefig(outfileprefix+'_cm.png')








	plot_P_R_curve(0)

	plt.tight_layout()
	plt.savefig(outfileprefix+'pos0_PRcurve.png')

	plot_P_R_curve(1)

	plt.tight_layout()
	plt.savefig(outfileprefix+'pos1_PRcurve.png')


testtosave=df.copy()
testtosave['mlprediction']=rf_predictions
testtosave['mlpredictProba']=rf_probs
testtosave.to_csv(outfileprefix+"_predicted.txt",sep="\t",index=False)






