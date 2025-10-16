#!/bin/bash

main() {
    local g

    B() {
        local a=$1
        local x

        A() {
            g=$x  # instead of g=$1, A now looks up x dynamically
        }

        R() {
            local m=$1
            echo "$x"
            x=$((x / 2))
            if (( x > 1 )); then
                R $((m + 2))
            else
                A
            fi
        }

        x=$((a * a))
        R 1
    }

    B 3
    echo "$g"
}

main
