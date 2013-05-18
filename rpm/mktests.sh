#!/bin/sh

cat <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<testdefinition version="1.0">
    <suite name="farstream-tests">
        <description>Farstream tests</description>
        <set name="farstram-unit-tests">
EOF

for testcase in $(cat tests/check/farstream-tests.list)
do
    testcase_name=$(echo $testcase|sed 's/\//_/')
    attributes="name=\"$testcase_name\""
    insignificant=`grep "^$testcase" tests/INSIGNIFICANT || true`
    if test -n "$insignificant"
    then
        continue
        attributes="$attributes insignificant=\"true\""
    fi
    cat <<EOF
        <case $attributes>
            <step>/opt/tests/farstream/bin/runTest.sh $testcase</step>
        </case>
EOF
done

cat <<EOF
        </set>
    </suite>
</testdefinition>
EOF
