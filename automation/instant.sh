source ~/.bashrc
CODE=~/thesis-code/automation/stdout_data_extractor.py
PREFIX=~/thesis-results/exp_set_1/one-vs-all/full-run/01-12-2013-
for INDEX in {0..9}
do
	printf "\n extracting training accuracies for test$[INDEX+1] on ${SYSTEMS[$INDEX]} ..."
	STDOUT_FILE=$PREFIX${SYSTEMS[$INDEX]}/test$[INDEX+1]/stdout.txt
	python $CODE -f $STDOUT_FILE
done

