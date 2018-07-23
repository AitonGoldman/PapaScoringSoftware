# Things to know before submitting a PR

## Try and create a github issue before starting any work
This isn't a requirment, but it's highly recommended.  This allows you to 
- track your work ( extremely helpfull when you have to a multi-week break from the code )
- give others an entry point if someone else has to take over the work
If you start working on an existing github issue, it's recommended that you assign yourself to the issue and track your work in it.  

## Get a review before merging 
This isn't a requirement, but the expectation is everyone will make an effort to get their code reviewed before merging it.  You can use the Slack instance to invite others to review your code.  If enough time passes and you can't get anyone to review your code, then alert a project in Slack.  

The flip side of this is the expectation that you will try to review other people's code.  Given the volunteer nature of the project, how well this gets done will depend on how many people are part of the project and how many people have the time to do it.  

## Keep you commits small
No one likes reviewing a 1000 line commit - and in the case of this project, large commits will make it much harder to get anyone to review your code.  Before you write any code, try and break up the work that needs to be done into chunks which can be committed seperately.  If you find yourself with a large commit (it happens sometimes) - don't just push it up - if you are not sure how to break it up, ask for help on the Slack instance.    

## Automated tests
All backend code must have automated tests.  If you are fixing a bug, a new test must be added to catch that bug in the future ( or an existing test must be modified ).   If you are modifying a feature, you might need to change existing tests.  If you are adding a new feature, you need to write new tests.  Please see (insert link here) for a brief introduction to how we do automated tests on this project.  

## No pushing to master
The master branch is protected and can not be directly pushed to.  In order to merge into master you must push up a branch, create a PR, get the PR approved and merge that PR.  

## Style
If you look at the existing code, you will notice a complete lack of style (this is one of things that needs fixed).  For the immediate future, the requirement is that you are internally consistent with your style.  It is encouraged (but not required) that you follow the PEP-8 style on the python side or use a tool like JSLint on the javascript side.  If you have any questions about style, ask on the Slack instance.    

