#!/bin/sh

export SRCDIR=/opt/tests/farstream/data/ 
export GST_CHECKS=test_nicetransmitter_with_filter

/opt/tests/farstream/bin/"$1"

e=$?
    case "$e" in
        (0)
            echo "PASS"
            ;;
        (*)
            echo "FAIL: ($e)"
            ;;
    esac

exit $e

