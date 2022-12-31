# editai-vim

Simple plugin to use the Edit API in OpenAI Codex.

## requirements

* vim with python3 enabled
* API Key from OpenAI

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

You can set the following variable to affect future requests:

```
:let g:editai_model = 'code-davinci-edit-001' or 'text-davinci-edit-001'. Default to code.
:let g:editai_temperature = 0.2
```
