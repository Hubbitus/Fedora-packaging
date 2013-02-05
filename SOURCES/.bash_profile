# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

# User specific environment and startup programs

PATH=$PATH:$HOME/bin:/usr/sbin:$HOME/bin/php_templates
BASH_ENV=$HOME/.bashrc
#USERNAME="root"
USERNAME="pasha"

export SVN=/mnt/sgtBarracuda/SVN_test/svn/repositories

export USERNAME BASH_ENV PATH
#export BASH_ENV PATH

export EDITOR=mcedit
