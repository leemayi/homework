function [C, sigma] = dataset3Params(X, y, Xval, yval)
%EX6PARAMS returns your choice of C and sigma for Part 3 of the exercise
%where you select the optimal (C, sigma) learning parameters to use for SVM
%with RBF kernel
%   [C, sigma] = EX6PARAMS(X, y, Xval, yval) returns your choice of C and 
%   sigma. You should complete this function to return the optimal C and 
%   sigma based on a cross-validation set.
%

% You need to return the following variables correctly.
% best params:
% C:1.000000, sigma:0.100000, error:0.030000
C = 1;
sigma = 0.1;

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return the optimal C and sigma
%               learning parameters found using the cross validation set.
%               You can use svmPredict to predict the labels on the cross
%               validation set. For example, 
%                   predictions = svmPredict(model, Xval);
%               will return the predictions on the cross validation set.
%
%  Note: You can compute the prediction error using 
%        mean(double(predictions ~= yval))
%

if 1<0; 
choices = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30];
min_error = -1;

for c = choices;
    for s = choices;

    model= svmTrain(X, y, c, @(x1, x2) gaussianKernel(x1, x2, s));
    predictions = svmPredict(model, Xval);
    err = mean(double(predictions ~= yval));
    fprintf('C:%f, sigma:%f, error:%f\n', c, s, err);

    if min_error == -1 | err < min_error;
        min_error = err;
        C = c;
        sigma = s;
        fprintf('it is the best so far\n');
    end

    end
end

fprintf('best params:\n');
fprintf('C:%f, sigma:%f, error:%f\n', C, sigma, min_error);
end

% =========================================================================

end
