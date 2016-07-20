PROTOS_LIB="protos_repository"

cd "$PROTOS_LIB"
printf 'N\n' | ./compile.py -l python -o ..

cd ..
