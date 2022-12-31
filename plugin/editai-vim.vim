if exists("g:loaded_editai_vim")
    finish
endif

py3 import sys
py3 import vim
py3 sys.path.append(vim.eval('expand("<sfile>:h")'))

fun! EditAIFunction(instruction)
py3 << EOT

from editai_vim import edit
edit(vim.eval("a:instruction"))

EOT
endfun

command! EditAI call EditAIFunction(input('Instruction: '))

nmap ,ea :EditAI<cr>

let g:loaded_editai_vim = 1
