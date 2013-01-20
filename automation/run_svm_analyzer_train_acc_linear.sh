source ~/.bashrc
CODE=~/thesis-code/automation/run_svm_analyzer_train_acc_linear.py
PREFIX=~/thesis-results/exp_set_1/one-vs-all-equal/full-run/01-13-2013-
#PREFIX=~/thesis-results/exp_set_1/one-vs-all/full-run/01-12-2013-
echo "running SVM analyzer ..."
for INDEX in {0..9}
do
	printf "\n calculating train_acc_linear test accuracy for test$[INDEX+1] on ${SYSTEMS[$INDEX]} ..."
	DECISION_VALUES_FILE=$PREFIX${SYSTEMS[$INDEX]}/test$[INDEX+1]/decision_values.csv
	STDOUT_FILE=$PREFIX${SYSTEMS[$INDEX]}/test$[INDEX+1]/stdout.txt
	python $CODE -sf $STDOUT_FILE -df $DECISION_VALUES_FILE
done

echo "SVM analyzer execution completed"
