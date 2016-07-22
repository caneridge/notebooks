git.txt

## Remove untracked files
  Remove directories and files
    git clean -xdf

## First time setup
  git config --global push.default current
  git config --global user.name 'Brian Jones'
  git config --global user.email 'Brian.Jones@twinspires.com'

## Create ssh key
  ssh-keygen -t rsa -C "comment" -f ~/.ssh/id_rsa_github -N ""
  ssh-keygen -t rsa -C "comment" -f ~/.ssh/id_rsa_ansible -N ""

.ssh/config

  Host github
    HostName github.cdinteractive.com
    User git
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/id_rsa_github

Test connection
  ssh -T git@github

## Clone repository
  git clone git@github.cdinteractive.com:twinspires/repo.git
  git clone https://github.cdinteractive.com/twinspires/repo.git

## List untracked files
  git ls-files --others

Stash files (tracked and -untracked)
  git stash -u

Show current commit
  git rev-parse HEAD

Find common ancestor
  git log -1 $(git merge-base branchA branchB)

Merge squash commit
  git checkout to_branch
  git merge --squash from_branch

  git log -1 $(git merge-base master R18tc)

Show current branch
  git show-branch

Show seconds date stamp of current commit
  git show -s --format=%at

Common ancestor of two branches:
  git merge-base origin/master origin/R18tc

Squash a branch into one commit
  checkout TO_LOCATION -b squash-branch
  git merge --squash branch-to-squash
  git commit -m "squashed version of branch"

Submodule
  # from the submodule folder
  git submodule init
  git submodule update

  Now, that you have submodule, check it's status:
  git status

  It is probably out of sync with master so just do:
  git checkout master

List files changed by a commit
  git diff-tree --no-commit-id --name-only -r COMMIT

Show commit that changed STRING
  git log -SSTRING

REBASE BRANCH
      +-work
    a-b-c

    git checkout work
    git rebase master

        +-work
    a-b-c

    git checkout master
    git merge work

    a-b-c-d

REBASE BRANCH OFF OF BRANCH

  a-b       master
  +-c-d     work1
      +-e   work2

  work1 is off of master
  work2 is off of work1
  Rebase work2 so it is off of master

  git rebase --onto master work1 work2

  a-b-e     master / work2
  +-c-d     work1

PUSH BRANCH
  git push origin BRANCH

GIT LOG RANGES
  Union of Y-left and Y-right
    git log left...right

  Y-right
    git log left..right
    git log ^left right
    git log right --not left

  Y-left
    git log right..left
    git log ^right left
    git log left --not right

  What am I about to push?
    git log ^origin/master HEAD

LIST MERGE CONFLICTS

  git diff --name-only --diff-filter=U

GIT LOG
  git log "--pretty=format:%h [%<(9)%cn] %s" --graph ^tags/3.17.1 HEAD
  git blame "--pretty=format:%h [%<(9)%cn]" tags/3.17.1 all.yml

  git blame --date=short tags/3.17.1 all.yml

HOTFIX PROCESS - Ryan
