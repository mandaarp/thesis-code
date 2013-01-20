source ~/.bashrc
CODE=~/thesis-code/experimental-code/svm-wise-test-accuracy.py
echo "running SVM analyzer ..."
for INDEX in {0..9}
do
	printf "\n calculating test accuracies for test$[INDEX+1] on ${SYSTEMS[$INDEX]} ..."
	DECISION_VALUES_FILE=~/thesis-results/exp_set_1/one-vs-all-equal/full-run/01-13-2013-${SYSTEMS[$INDEX]}/test$[INDEX+1]/decision_values.csv
	python $CODE -f $DECISION_VALUES_FILE
done

echo "SVM analyzer execution completed"
