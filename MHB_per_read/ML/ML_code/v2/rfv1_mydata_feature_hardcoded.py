import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import sys
import matplotlib.pyplot as plt
import pickle

RSEED = 0

# Load in data
irfinfile=sys.argv[1]
mtest_size=float(sys.argv[2])
df = pd.read_csv(irfinfile,sep="\t")  #'https://s3.amazonaws.com/projects-rf/clean_data.csv'

outfileprefix=irfinfile+"_testsize_"+str(mtest_size)

# Full dataset: https://www.kaggle.com/cdc/behavioral-risk-factor-surveillance-system

# Extract the labels

if mtest_size>0:

    labels = np.array(df.pop('label'))

    

    # 30% examples in test data
    train, test, train_labels, test_labels = train_test_split(df,
                                             labels, 
                                             stratify = labels,
                                             test_size = mtest_size, 
                                             random_state = RSEED)

else:
    train=df.drop("label",axis=1)
    train_labels=df["label"].copy()
    test=train.copy()
    test_labels=train_labels.copy()


traintosave=train.copy()
traintosave['label']=train_labels
testtosave=test.copy()
testtosave['label']=test_labels

traintosave.to_csv(outfileprefix+"_train.txt",sep="\t",index=False)
testtosave.to_csv(outfileprefix+"_test.txt",sep="\t",index=False)


train=(traintosave[['acceptedCpGLen','notacceptedCpGLen','len_hypolist','len_hyperlist','fraglength']]).copy()
test=(testtosave[['acceptedCpGLen','notacceptedCpGLen','len_hypolist','len_hyperlist','fraglength']]).copy()


# Imputation of missing values
#train = train.fillna(train.mean())
#test = test.fillna(test.mean())

# Features for feature importances
features = list(train.columns)

# Create the model with 100 trees
model = RandomForestClassifier(n_estimators=100, 
                               random_state=RSEED, 
                               max_features = 'sqrt',
                               n_jobs=-1)

# Fit on training data
model.fit(train, train_labels)

fig = plt.figure()
plt.barh(train.columns, model.feature_importances_)
plt.xlabel("Random Forest Feature Importance")
plt.tight_layout()
plt.savefig(outfileprefix+'_featureimportance.png')
plt.close(fig)


fig = plt.figure()
sorted_idx = model.feature_importances_.argsort()
plt.barh(train.columns[sorted_idx], model.feature_importances_[sorted_idx])
plt.xlabel("Random Forest Feature Importance")
plt.tight_layout()
plt.savefig(outfileprefix+'_sortedfeatureimportance.png')
plt.close(fig)




n_nodes = []
max_depths = []

# Stats about the trees in random forest
for ind_tree in model.estimators_:
    n_nodes.append(ind_tree.tree_.node_count)
    max_depths.append(ind_tree.tree_.max_depth)
    
print(f'Average number of nodes {int(np.mean(n_nodes))}')
print(f'Average maximum depth {int(np.mean(max_depths))}')

# Training predictions (to demonstrate overfitting)
train_rf_predictions = model.predict(train)
train_rf_probs = model.predict_proba(train)[:, 1]

# Testing predictions (to determine performance)
rf_predictions = model.predict(test)
rf_probs = model.predict_proba(test)[:, 1]



from sklearn.metrics import precision_score, recall_score, roc_auc_score, roc_curve


# Plot formatting
plt.style.use('fivethirtyeight')
plt.rcParams['font.size'] = 18

def evaluate_model(predictions, probs, train_predictions, train_probs):
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
    
    train_results = {}
    train_results['recall'] = recall_score(train_labels, train_predictions)
    train_results['precision'] = precision_score(train_labels, train_predictions)
    train_results['roc'] = roc_auc_score(train_labels, train_probs)
    
    for metric in ['recall', 'precision', 'roc']:
        print(f'{metric.capitalize()} Baseline: {round(baseline[metric], 2)} Test: {round(results[metric], 2)} Train: {round(train_results[metric], 2)}')
    
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


evaluate_model(rf_predictions, rf_probs, train_rf_predictions, train_rf_probs)
plt.savefig(outfileprefix+'_roc_auc_curve.png')

from sklearn.metrics import confusion_matrix
import itertools


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

# Confusion matrix

cm = confusion_matrix(test_labels, rf_predictions)
plot_confusion_matrix(cm, classes = ['positive', 'negative'],
                      title = 'Confusion Matrix')

plt.savefig(outfileprefix+'_cm.png')





from sklearn.metrics import plot_precision_recall_curve
def plot_P_R_curve(poslabel):
    plot_precision_recall_curve(model, test, test_labels,pos_label=poslabel, name = 'rf')


plot_P_R_curve(0)

plt.tight_layout()
plt.savefig(outfileprefix+'pos0_PRcurve.png')

plot_P_R_curve(1)

plt.tight_layout()
plt.savefig(outfileprefix+'pos1_PRcurve.png')

model.feature_names = features
with open(outfileprefix+"_model",'wb') as f:
    pickle.dump(model,f)








