# .bashrc

# Addon file from Hubbitus-config rpm for base confugiration

# Nice to long time test: gotar, modarcon16*, modarin256* (with root), nicedark, xoria256 + transparent background in ini
# Unfortunately CentOS versions of MC have no modarin256* themes, fallback on gotar
alias mc='if [ $TERM == "linux" ]; then mc -x --skin=gotar; else TERM=xterm-256color mc -x --skin=$( [ -f /usr/share/mc/skins/modarin256root-defbg.ini ] && echo modarin256root-defbg || echo gotar ); fi'

alias yum='LANG=en_US.utf8 yum'
alias dnf='LANG=en_US.utf8 dnf'

alias bmon='bmon -o curses:gheight=20'

export EDITOR=mcedit

export ELMON=cmMvtanld
