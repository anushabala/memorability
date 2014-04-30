#Written by: Anusha Balakrishnan
#Date: 4/30/14
from libsvm import svmutil
from libsvm.svm import *
from libsvm.svmutil import *

def cross_validation():
    models = []
    for i in range(1,6):
        y, x = svm_read_problem('create_datasets/fv_train%d.dat' % i)
        prob = svm_problem(y,x)
        param = svm_parameter()
        param.C = 20
        param.kernel_type= LINEAR
        model = svm_train(prob, param)
        models.append(model)

        y, x = svm_read_problem('create_datasets/fv_dev%d.dat' % i)
        p_labels, p_acc, p_vals = svm_predict(y, x, model)

def cross_domain():
    y, x = svm_read_problem('create_datasets/fv_combined.dat')
    prob = svm_problem(y,x)
    param = svm_parameter()
    param.C = 20
    param.kernel_type= LINEAR
    model = svm_train(prob, param)

    y,x = svm_read_problem('create_datasets/fv_Advertising.dat')
    p_labels, p_acc, p_vals = svm_predict(y, x, model)

cross_domain()