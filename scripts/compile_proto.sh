PROTOS_LIB="POGOProtos"
PROTOCOL_OUT="protocol"
FIX_PY_IMPORTS_CODE="import os\nimport sys\nsys.path.append(os.path.dirname(__file__))"

cd "$PROTOS_LIB"
./compile.py -l python -o ../"$PROTOCOL_OUT"

cd ..


recursive_fixing() {
	for i in "$1"*/; do
		if [ -d "$i" ]; then
			echo "Setting up module $i"
			echo "" > "${i}__init__.py"
			recursive_fixing "$i"
		fi
	done
}

recursive_fixing "${PROTOCOL_OUT}/"

printf "$FIX_PY_IMPORTS_CODE" > "$PROTOCOL_OUT/__init__.py"
