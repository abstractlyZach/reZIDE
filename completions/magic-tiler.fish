function _magic_tiler_completion;
    set -l response;

    for value in (env _MAGIC_TILER_COMPLETE=fish_complete COMP_WORDS=(commandline -cp) COMP_CWORD=(commandline -t) magic-tiler);
        set response $response $value;
    end;

    for completion in $response;
        set -l metadata (string split "," $completion);

        if test $metadata[1] = "dir";
            __fish_complete_directories $metadata[2];
        else if test $metadata[1] = "file";
            __fish_complete_path $metadata[2];
        else if test $metadata[1] = "plain";
            echo $metadata[2];
        end;
    end;
end;

complete --no-files --command magic-tiler --arguments "(_magic_tiler_completion)";
