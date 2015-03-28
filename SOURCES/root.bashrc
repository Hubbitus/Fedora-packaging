# .bashrc

# Addon file from Hubbitus-config rpm for base confugiration

# Nice to long time test: gotar, modarcon16*, modarin256* (with root), nicedark, xoria256 + transparent background in ini
alias mc='if [ $TERM == "linux" ]; then mc -x --skin=gotar; else TERM=xterm-256color mc -x --skin=modarin256root-defbg; fi'

alias yum='LANG=en_US.utf8 yum'

alias bmon='bmon -o curses:gheight=20'

export EDITOR=mcedit

export ELMON=cmMvtanld
