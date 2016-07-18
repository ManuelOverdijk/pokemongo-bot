PROTOS_LIB="POGOProtos"
PROTOCOL_OUT="protocol"
FIX_PY_IMPORTS_CODE="import os\nimport sys\nsys.path.append(os.path.dirname(__file__))"

cd "$PROTOS_LIB"
./compile.py -l python -o ../"$PROTOCOL_OUT"

cd ..

for d in "$PROTOCOL_OUT"/*/; do
	echo "" > "${d}__init__.py"
	echo "Setting up module $d"
done

printf "$FIX_PY_IMPORTS_CODE" > "$PROTOCOL_OUT/__init__.py"
