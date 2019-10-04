#!/bin/sh

let port=8000

usage()
{
	echo "Usage: $(basename $0) [-p port]" >&2
	exit 1
}

while getopts 'p:h' OPTION; do
	case "$OPTION" in
		p)
			let port=$(($OPTARG))
			;;
		?)
			usage
			;;
	esac
done
shift "$(($OPTIND -1))"

python3 "server.py" "-p" "$port"
