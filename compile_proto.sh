PROTOS_LIB="POGOProtos"
PROTOCOL_OUT="protocol"
INIT="__init__.py"

cd "$PROTOS_LIB"
./compile.py -l python -o ../"$PROTOCOL_OUT"

cd ..

for d in "$PROTOCOL_OUT"/*/; do
	echo "" > "${d}__init__.py"
	echo "Setting up module $d"
done

printf "import os\nimport sys\nsys.path.append(os.path.dirname(__file__))" > "$PROTOCOL_OUT/__init__.py"
