_magic_tiler_completion() {
    local IFS=$'\n'
    local response

    response=$(env COMP_WORDS="${COMP_WORDS[*]}" COMP_CWORD=$COMP_CWORD _MAGIC_TILER_COMPLETE=bash_complete $1)

    for completion in $response; do
        IFS=',' read type value <<< "$completion"

        if [[ $type == 'dir' ]]; then
            COMREPLY=()
            compopt -o dirnames
        elif [[ $type == 'file' ]]; then
            COMREPLY=()
            compopt -o default
        elif [[ $type == 'plain' ]]; then
            COMPREPLY+=($value)
        fi
    done

    return 0
}

_magic_tiler_completion_setup() {
    complete -o nosort -F _magic_tiler_completion magic-tiler
}

_magic_tiler_completion_setup;
