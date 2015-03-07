OUT="../ipp-dka-test/out/"
IN="../ipp-dka-test/in/"
TEST_SCRIPT="../ipp-dka-test/test.sh"
TEST_TO_OUT="out/"
SCRIPT="dka.py"
INTERPRETER="python3"
INPUT="in"
ARGUMENTS='--analyze-string='
FIRST_NUMBER=1

files=($(ls -d $OUT* | sort -V -r))
file=${files[0]}
last=`echo $file|sed 's/[^0-9]//g'`
if [[ $last == "''" || "$last" < "$FIRST_NUMBER" ]]; then
	last=${FIRST_NUMBER}-1
fi

((last++))
$INTERPRETER $SCRIPT $ARGUMENTS 1> $OUT"test"$last".out" < $INPUT
out=$?

cp $INPUT ${IN}"test"${last}".in"

echo "run_test"  \'$TEST_TO_OUT"test"$last".out"\'  \""$out"\" \'"$ARGUMENTS --input="${IN}"test"${last}".in"\' \'$1\'   >> $TEST_SCRIPT


