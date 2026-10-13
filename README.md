# Multi-sensory Based Robot Dynamic Manipulation

These repository contains the content for the course Multi-sensory Based Robot Dynamic manipulation.
It will be updated throughout the Winter 2026/27 semester.

## Materials
The lecture slides and tutorial instructions are accessible from the [wiki page](https://gitlab.lrz.de/msbrdm/msbrdm-lecture-2026/-/wikis/home).

## Q&A

We use the [issues page](https://gitlab.lrz.de/msbrdm/msbrdm-lecture-2026/-/issues) for questions and discussions.

Feel free to discuss among yourself, or tag us with a question about lecture questions, doubts about tutorials etc., but please refrain from posting your solutions.

## Homework

You will use this [git](https://git-scm.com/) repository for solving and submitting homeworks. 

Your personal "fork" of the [base repo](https://gitlab.lrz.de/msbrdm/msbrdm-lecture-2026) (`<your_name>_ws`) contains all the code.

You will [pull](https://git-scm.com/docs/git-pull) new assignments from our base repo (`upstream`) and [push](https://git-scm.com/docs/git-push) your changes to your personal repo (`origin`) to submit your solutions. That way, you "download" our new assignment from the base repo to your computer and then "upload" your solution to your GitLab repo for grading.

#### Request your repository

- Please send a email to [msbrdm-lecture.ics@xcit.tum.de]() to request access to the repository, if you don't have the access yet.
- We will create a forked repository for you and add you as developer.

#### Setup your repository

Once you have access to the forked repository, you can clone it to local. Navigate to the page of your workspace and clone with

```console
$ git clone git@gitlab.lrz.de:msbrdm/student-workspaces-2026/<your_name>_ws.git
```

Note: we recommend to use [ssh keys](https://docs.gitlab.com/ee/user/ssh.html) to communicate with the remote repos to avoid typing your username and password each time.

#### Adding upstream

In order to regularly pull the new assignments and any other changes (bugfixes), you must add the original [base repo](https://gitlab.lrz.de/msbrdm/msbrdm-lecture-2026) as `upstream` remote.

To do this, navigate to your cloned project's directory and use the following commands from the console:

First check the original setup with:

```console
$ git remote -v
```

The output should be:

```console
> origin  git@gitlab.lrz.de:msbrdm/student-workspaces-2026/<your_name>_ws.git (fetch)
> origin  git@gitlab.lrz.de:msbrdm/student-workspaces-2026/<your_name>_ws.git (push)
```

which tells us, that remote with the name origin (your GitLab repo) points to your local repo. To add the [base repo](https://gitlab.lrz.de/msbrdm/msbrdm-lecture-2026) use:

```console
$ git remote add upstream git@gitlab.lrz.de:msbrdm/msbrdm-lecture-2026.git
```

This command adds a the base repo as `upstream`. Again, you can verify that it was added:

```console
$ git remote -v
> origin  git@gitlab.lrz.de:msbrdm/student-workspaces-2026/<your_name>_ws.git (fetch)
> origin  git@gitlab.lrz.de:msbrdm/student-workspaces-2026/<your_name>_ws.git (push)
> upstream  git@gitlab.lrz.de:msbrdm/msbrdm-lecture-2026.git (fetch)
> upstream  git@gitlab.lrz.de:msbrdm/msbrdm-lecture-2026.git (push)
```

With this configuration, your local `git` repo can now talk to two independent remote `git` repositories:

- `origin` is your repo on GitLab, where you commit your homework results
- `upstream` is our repo on GitLab, where we publish new assignments

#### Getting new assignments

If you want to get the new assignments or other changes, go to your project directory and use:

```console
$ git pull upstream main    # download and merge our changes to your local repo
```

This first connects to our server and downloads the information from the base project, where we publish the homeworks to. Then, it merges our `upstream/main` contents into your local `main` branch. For new assignments, we always use new files, so this should work without any merge conflicts.

However, if both of us changed the same file, a merge conflict might happen if the changes aren't compatible, in which case you need to resolve the conflict before you can start working.

#### Submit your homework

Generally, this is the work flow of doing your home work

```console
$ git pull upstream main          # get the new homework assignment from us
# ~~ do the homework ~~
$ git status                      # see how git thinks about your files
$ git add .                       # add the changes you want to commit
$ git commit -m "my submission"   # create the commit
$ git push origin main            # upload the changes to your GitLab repository
```

You can make as many commits as you want before the deadline.

After you finish, get your latest commits with:

```console
$ git log
```

Copy the your latest commit information (see example below) and send us via email [msbrdm-lecture.ics@xcit.tum.de]() before the deadline.

```
> commit 3e20d97cf20a9e1c6b3be0dfaf89ee4c1715c3bd (HEAD -> main, origin/main, origin/HEAD)
> Author: Wenlan Shen <wenlan.shen@tum.de>
> Date:   Tue Oct 17 23:30:11 2026 +0200

    T1 submission 
  ...
```

For each tutorial, we will grade the commit you send with email. You could still make changes afterwards to make the later tutorials work, but they will not be counted in grading. Note that the submission after the deadline can only get at most 90% of the total points, and 80% for longer delays (> 1 week).


## Docker Image of Ubuntu 24.04 and ROS jazzy
We provide a docker image for those who don't have Ubuntu 24.04 and ROS 2 Jazzy installed.

### Setup
#### Prerequisites
- Make sure you have the latest docker installed before starting: https://docs.docker.com/engine/install/ubuntu/
- Install Nvidia-Container-SDK if you have Nvidia GPU.
- Install Docker and Dev Containers extensions in VS Code.

#### Pull the docker image
- Pull the docker image
```bash
# PULL
docker login gitlab.lrz.de:5005
docker pull gitlab.lrz.de:5005/msbrdm/msbrdm-lecture-2026/tum-ics-ros:jazzy-ics-msbrdm-devel-vscode
docker tag gitlab.lrz.de:5005/msbrdm/msbrdm-lecture-2026/tum-ics-ros:jazzy-ics-msbrdm-devel-vscode tum-ics-ros:jazzy-ics-msbrdm-devel-vscode
```
#### Usage
- Open your workspace in VS code.
- There should be a pop-up asking if you want to reopen in devcontainer -> click yes. If not, press Ctrl + Shift + p, type and find command "Dev containers: Rebuild and Reopen in Container" and click it.
- You should see "Dec Container: msbrdm_tutorial_ws" on the lower left corner of your VS Code window, if the build is successful.
- Note: if you don't have Nvidia GPU, comment out the tags `--runtime=nvidia` (line 23) in `.devcontainer/devcontainer.json`.
- If you want to use the terminals in VS Code, source the setup script in the terminals
```bash
source setup_devcont.sh
```
- If you want to attach your host terminals to the docker container, add the following to your **host** `~/.bash_aliases`
```bash
devcont_bash()
{
    local CONT_NAME=$1
    docker exec -it $CONT_NAME runuser -u devel -- bash -c "cd \$CONT_PWD && export CONT_PWD_AUTO_SOURCE_SETUP=true && bash"
}

devcont_bash_complete()
{
    local contNames=($(docker ps --format "{{.Names}}"))

    COMPREPLY=()

    local word="${COMP_WORDS[COMP_CWORD]}"

    if [ "$COMP_CWORD" -eq 1 ]; then
        COMPREPLY=($(compgen -W "${contNames[*]}" -- "$word"));
    fi
}
```
Then you can use the following command to access the running container on your local terminals
```bash
devcont_bash <your_name>_ws_devcont
```
