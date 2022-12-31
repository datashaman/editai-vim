# editai-vim

Simple plugin to use the Edit API in OpenAI Codex.

## installation

Install `datashaman/editai-vim` with _Vim-Plug_, _Vundle_, etc.

Set the OpenAI API Key in your environment and export it:
```
export OPENAI_API_KEY=yourkeyhere
```

## usage

The plugin calls the OpenAI edit API with the current buffer contents as input.

You are prompted for the instruction, which will guide the AI in changing your code.

If you don't like the changes, use undo as usual.

The command is used as follows:

```
:EditAI
```

`,ea` has been mapped to call the command.
