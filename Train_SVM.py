#Written by: Anusha Balakrishnan
#Date: 4/30/14
from libsvm import svmutil
from libsvm.svm import *
from libsvm.svmutil import *

def libsvm_cv():
    y, x = svm_read_problem('create_datasets/fv_noBOW_combined.dat')
    prob = svm_problem(y,x)
    param = svm_parameter()
    param.C = 20
    param.kernel_type= LINEAR
    param.cross_validation = 5
    acc = svm_train(prob, param)
    print acc
def cross_validation():
    models = []
    accuracies = []
    for i in range(1,6):
        y, x = svm_read_problem('create_datasets/fv_trainnoBOW%d.dat' % i)
        prob = svm_problem(y,x)
        param = svm_parameter()
        param.C = 1
        param.kernel_type= LINEAR
        model = svm_train(prob, param)
        models.append(model)

        y, x = svm_read_problem('create_datasets/fv_devnoBOW%d.dat' % i)
        p_labels, p_acc, p_vals = svm_predict(y, x, model)
        accuracies.append(p_acc)

    total_acc = sum([int(accuracies[i][0]) for i in range(0, len(accuracies))])

    print "\nAverage cross-validation accuracy: %f" % (float(total_acc)/len(accuracies))
    # y, x = svm_read_problem('create_datasets/fv_test.dat')
    # p_labels, p_acc, p_vals = svm_predict(y, x, model)
def get_f1(labels, path):
    fv_file = file(path, 'r')
    lines = fv_file.readlines()
    i =0
    total_pred_p = 0
    true_p = 0
    total_actual_p = 0
    print labels
    for line in lines:

        actual_label = int(line.strip()[0])
        pred_label = labels[i]
        if actual_label == 1:
            total_actual_p+=1
        if pred_label == 1:
            total_pred_p+=1
        if actual_label == pred_label and pred_label==1:
            true_p+=1
        i+=1
    fv_file.close()

    prec = float(true_p)/total_pred_p
    rec = float(true_p)/total_actual_p
    f1_score = 2 * (prec*rec)/(prec+rec)
    print "Precision: %f" % prec
    print "Recall: %f" % rec
    print "F1 score: %f" %f1_score


def cross_domain(feature_set, test_set):
    y, x = svm_read_problem('create_datasets/fv%s_combined.dat' % feature_set)
    prob = svm_problem(y,x)
    param = svm_parameter()
    param.C = 2
    kerneltypes = [LINEAR,RBF, SIGMOID]
    all_labels = []
    for kernel in kerneltypes:
        param.kernel_type= kernel
        model = svm_train(prob, param)
        svm_save_model('model.dat', model)
        y,x = svm_read_problem('create_datasets/fv%s_%s.dat' %(feature_set, test_set))
        p_labels, p_acc, p_vals = svm_predict(y, x, model)
        # if kernel==RBF:
        get_f1(p_labels, 'create_datasets/fv%s_%s.dat' % (feature_set, test_set))
#
# cross_validation()
cross_domain('_baseline', 'Political')
# libsvm_cv()
