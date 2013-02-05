# .bashrc

# Source global definitions
#if [ -f /etc/bashrc ]; then
	. /etc/bashrc
#fi

PATH=$PATH:$HOME/bin:/usr/sbin:$HOME/bin/php_templates

# User specific aliases and functions

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

alias ndrpm='rpm -Uhv --excludedocs'
alias rf='rpm -qf'
alias rq='rpm -q'

alias grep='grep --color'
alias egrep='egrep --color'
alias fgrep='fgrep --color'

alias ll='ls -l --color=auto'

alias yum='nice -n19 yum'
#alias rpmbuild='nice -n18 rpmbuild --target=athlon | egrep "Записан:|Wrote:" | cut -d" " -f2 | xargs -r rpmlint'
rpmbuild (){
nice -n18 rpmbuild "$@" | egrep "Записан:|Wrote:" | cut -d" " -f2 | xargs -r rpmlint
}

alias rtorrent='ionice -c3 nice -n17 rtorrent'

#alias mplayer='mplayer -framedrop -zoom -fs'
alias gmplayer='gmplayer -framedrop -zoom'

#alias screen='screen -OaUx main || screen -OaU -S main'
#alias screen-remote='/usr/bin/screen -OaUx Remote || /usr/bin/screen -OaU -S Remote -c /home/pasha/.screenrc-remote'

# Function instead of alis to behave identically on remote aned local execute
# http://www.thelinuxlink.net/pipermail/lvlug/2005-July/014629.html
function screen(){
	/usr/bin/screen -OaUx Main $@ || /usr/bin/screen -OaU -S Main $@
}

function screen-remote(){
	/usr/bin/screen -OaUx Remote || /usr/bin/screen -OaU -S Remote -c /home/pasha/.screenrc-remote
}

alias ssh-agent='eval `SSH_AGENT_REUSE_MUST_BE_SOURCED='' /home/pasha/bin/ssh-agent-reENV.bash`'

alias sus="su -l -c 'screen -x || screen'"

alias rsync_s='. ~/.rsync_shared_options ; rsync $RSYNC_SHARED_OPTIONS'

alias grin='grin --force-color'

alias св=cd

#alias svn=colorsvn

alias t='cd ~/temp'

function sshs(){
ssh -t $@ 'screen -x || screen'
}

function whilesshs(){
whilessh -t $@ 'screen -x || screen'
}

#http://rusmafia.org/linux/node/21
shopt -s cdspell

#+3 http://tigro.info/blog/index.php?id=418
shopt -s histappend
#PROMPT_COMMAND='history -a'

#http://stasikos.livejournal.com/tag/mc Remove trash from MC
#export HISTCONTROL="ignoredups"
export HISTCONTROL=ignoreboth

complete -W "`awk 'BEGIN {FS=" |,"} {print $1}' ~/.ssh/known_hosts | sort`" ssh

#Auto start ssh-agent. http://rusmafia.org/linux/ssh-agent-shell-startup
##[ ! -S ~/.ssh/ssh-agent ] && eval `/usr/bin/ssh-agent -a ~/.ssh/ssh-agent`
##[ -z $SSH_AUTH_SOCK ] && export SSH_AUTH_SOCK=~/.ssh/ssh-agent
## Auto start now performed by local alias with reusing existence socket!

#ssh-agent #just execute, alias redefined before.
	# On my home machine alias before defined (znd alias show it properly), but in this line (or file?)
	# call by it is not worked :( See example ~/bin/SHARED/examples/bash-alias.test
	# So, directly get and exec value:
	[ alias ssh-agent &>/dev/null ] && $( alias ssh-agent | sed -r "s/^alias ttt='(.*)'/\1/" )


# http://wiki.clug.org.za/wiki/Colour_on_the_command_line#Colourful_manpages_.28RedHat_style.29
# For colourful man pages (CLUG-Wiki style)
export LESS_TERMCAP_mb=$'\E[01;31m'
export LESS_TERMCAP_md=$'\E[01;31m'
export LESS_TERMCAP_me=$'\E[0m'
export LESS_TERMCAP_se=$'\E[0m'
export LESS_TERMCAP_so=$'\E[01;44;33m'
export LESS_TERMCAP_ue=$'\E[0m'
export LESS_TERMCAP_us=$'\E[01;32m'

SVN='svn+ssh://x-www.info/mnt/sgtBarracuda/SVN_test/svn/repositories/'

export EDITOR=mcedit