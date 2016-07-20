PROTOS_LIB="protos_repository"

cd "$PROTOS_LIB"
printf 'N\n' | python ./compile_single.py -l python -o ..

cd ..
